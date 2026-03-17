from typing import Optional

import arviz as az
import pyro
import pyro.infer
import pyro.infer.autoguide
import pyro.optim
import sympy as sp
import torch
from pyro.infer import (
    MCMC,
    NUTS,
    JitTrace_ELBO,
    Predictive,
    RandomWalkKernel,
    Trace_ELBO,
)
from pyro.infer.autoguide import init_to_value
from pyro.infer.mcmc.util import select_samples

from equayes.core.pyro_backend import sympy_to_pyro as sp_to_pyro
from equayes.core.pyro_backend import utils as pyro_utils
from equayes.core.sympy_backend import utils as sp_utils
from equayes.utils import log

logger = log.getLogger(__name__)


class Equayes:
    """A scikit-learn style estimator for performing Bayesian inference on deterministic equations.

    This class bridges the gap between symbolic mathematics and probabilistic machine learning.
    It takes a deterministic mathematical model (defined as a SymPy expression), automatically
    identifies its numeric constants, and replaces them with learnable parameters. It then
    compiles this symbolic expression into a probabilistic Pyro model.

    Via the scikit-learn like API (fit, predict, score), users can easily apply Markov Chain
    Monte Carlo (MCMC) methods or Variational Inference (VI) to fit the symbolic model to empirical data. This allows
    to not only find optimal parameter values, but also quantify uncertainty, extract posterior
    distributions, and generate predictive distributions with confidence bounds.

    Typical Use Cases:
        - Calibrating physics-based or first-principles equations with noisy data.
        - Adding uncertainty quantification to equations discovered via Symbolic Regression.
        - Evaluating the robustness of a mathematical model's parameters.
    """

    def __init__(
        self,
        expr: sp.Expr,
        input_symbols: list[sp.Symbol],
        output_dim=1,
        inference_method_name: str = "mcmc",
        kernel_name: str = "nuts",
        mcmc_samples: int = 1000,
        mcmc_warmup_samples: int = 1000,
        mcmc_chains: int = 1,
        mcmc_initial_step_size: float = 1e-2,
        vi_iter: int = 1000,
        vi_lr: float = 1e-2,
        vi_lrd: float = 1.0,
        vi_particles: int = 1,
        jit_compile: bool = False,
        initial_params: Optional[dict[str, torch.Tensor]] = None,
    ) -> None:
        """Initializes the Equayes model for Bayesian inference on SymPy expressions.

        Args:
            expr (sp.Expr): The symbolic mathematical expression representing the core model structure.
                All numeric constants in the expression are automatically detected and replaced
                with learnable parameters during initialization.

            input_symbols (list[sp.Symbol]): A list of SymPy symbols corresponding to the input
                features (independent variables) of the model. The order of the symbols must
                match the column order of the input tensor provided during fitting.

            output_dim (int, optional): The dimensionality of the model's output. This determines
                the shape of the likelihood and predictive samples. Defaults to 1.

            inference_method_name (str, optional): The inference strategy used to fit the model.
                Supported options are:
                - "mcmc": Markov Chain Monte Carlo sampling
                - "vi": Variational Inference
                Defaults to "mcmc".

            kernel_name (str, optional): The MCMC transition kernel used when
                `inference_method="mcmc"`. Supported options are:
                - "nuts": No-U-Turn Sampler (Hamiltonian Monte Carlo variant)
                - "random_walk": Random Walk Metropolis-Hastings
                Defaults to "nuts".

            mcmc_samples (int, optional): The number of posterior samples to draw
                after warm-up when using MCMC. Ignored if `inference_method="vi"`.
                Defaults to 1000.

            mcmc_warmup_samples (int, optional): The number of warm-up (burn-in) steps
                for MCMC sampling. These samples are discarded and used only for
                adaptation of the sampler. Ignored if `inference_method="vi"`.
                Defaults to 1000.

            mcmc_chains (int, optional): The number of independent MCMC chains to run.
                Increasing this value improves convergence diagnostics but increases
                computational cost. Ignored if `inference_method="vi"`.
                Defaults to 1.

            mcmc_initial_step_size (float, optional): The initial step size for the MCMC
                sampler. For NUTS, this serves as the starting point for step size
                adaptation. For Random Walk, it controls the proposal scale.
                Ignored if `inference_method="vi"`. Defaults to 1e-2.

            vi_iter (int, optional): The number of optimization iterations used
                when `inference_method="vi"`. Ignored if `inference_method="mcmc"`.
                Defaults to 1000.

            vi_lr (float, optional): The learning rate for the optimizer used in
                Variational Inference. Controls the step size of gradient-based
                updates. Ignored if `inference_method="mcmc"`.
                Defaults to 1e-2.

            vi_lrd (float, optional): The exponential learning rate decay for the optimizer used in
                Variational Inference. Controls the decay of the step size of the optimizer.
                Ignored if `inference_method="mcmc"`.
                Defaults to 1. (no decay).

            vi_particles (int, optional): The number of samples of the variational
                distribution (called particles) used to estimate the Evidence
                Lower Bound (ELBO) during Variational Inference. Higher values
                reduce gradient variance but increase computational cost.
                Ignored if `inference_method="mcmc"`.
                Defaults to 1.

            jit_compile (bool, optional): If True, enables Just-In-Time (JIT)
                compilation for supported inference components to potentially
                improve execution speed. Defaults to False.

            initial_params (Optional[dict[str, torch.Tensor]]): CURRENTLY IGNORED. Custom, per-latent site
                initialization of numerical constants that are converted to random variables in expr.
                If not provided, the initial value is the constant given in the expression.
                Defaults to None.

        """

        self.expr_sp = expr
        self.input_symbols = input_symbols
        self.inference_method_name = inference_method_name  # in (mcmc, vi)
        self.kernel_name = kernel_name  # in (nuts, random_walk)
        self.mcmc_samples = mcmc_samples
        self.mcmc_warmup_samples = mcmc_warmup_samples
        self.mcmc_chains = mcmc_chains
        self.mcmc_initial_step_size = mcmc_initial_step_size
        self.vi_iter = vi_iter
        self.vi_lr = vi_lr
        self.vi_lrd = vi_lrd
        self.n_particles = vi_particles
        self.jit_compile = jit_compile

        if initial_params is not None:
            logger.warning("Parameter 'initial_params' is ignored in the current version and will not have any effect.")
        self.initial_params = None

        self.mcmc_ = None
        self.svi_ = None

        self._expr_sp_parameterized, self._exp_param_values = sp_utils.replace_floats_in_print_order(self.expr_sp)
        self._pyro_model = sp_to_pyro.create_pyro_model(
            self._expr_sp_parameterized,
            self.input_symbols,
            list(self._exp_param_values.keys()),
            output_dim=output_dim,
        )
        self._setup_inference()

    def _setup_inference(self) -> None:
        """Setup Inference - either MCMC or VI.

        Args:
            None
        """
        self.initial_params = pyro_utils.get_initial_param_dict(self._exp_param_values, n_chains=self.mcmc_chains)

        match self.inference_method_name:
            case "mcmc":
                self._setup_mcmc()
            case "vi":
                self._setup_svi()
            case _:
                raise NotImplementedError(
                    f"inference_method_name '{self.inference_method_name}' not implemented. Valid inference_method_name: 'mcmc', 'vi'."
                )

    def _setup_mcmc(self):
        """Configures the MCMC inference kernel and sampler based on the provided initialization parameters."""

        match self.kernel_name:
            case "nuts":
                self._kernel = NUTS(
                    self._pyro_model,
                    jit_compile=self.jit_compile,
                    step_size=self.mcmc_initial_step_size,
                )
            case "random_walk":
                self._kernel = RandomWalkKernel(
                    self._pyro_model,
                    init_step_size=self.mcmc_initial_step_size,
                )
            case _:
                raise NotImplementedError(f"Kernel '{self.kernel_name}' not implemented. Valid kernels: 'nuts', 'random_walk'.")

    def _setup_svi(self):
        """Configures the VI inference kernel and optimizer based on the provided initialization parameters."""

        self._guide = pyro.infer.autoguide.AutoMultivariateNormal(
            self._pyro_model, init_loc_fn=init_to_value(values=self.initial_params)
        )
        self._optim = pyro.optim.ClippedAdam({"lr": self.vi_lr, "lrd": self.vi_lrd ** (1 / self.vi_iter)})
        if self.jit_compile:
            self._loss = JitTrace_ELBO(num_particles=self.n_particles, vectorize_particles=True)
        else:
            self._loss = Trace_ELBO(num_particles=self.n_particles, vectorize_particles=True)

    def fit(self, X: torch.Tensor | None, y: torch.Tensor) -> None | list:
        """Fits the Bayesian model to the provided data using the configured inference method.

        Args:
            X (torch.Tensor | None): The input feature data of shape (batch, features).
            y (torch.Tensor): The target output data of shape (batch, output_dim).
        """
        pyro.clear_param_store()
        if X is not None:
            assert X.dim() == 2 and "X shape must be (batch, features)"
        assert y.dim() == 2 and "y shape must be (batch, features)"
        match self.inference_method_name:
            case "mcmc":
                if self.mcmc_ is None:  #  allows to provide a user defined MCMC instance, too.
                    self.mcmc_ = MCMC(
                        self._kernel,
                        num_samples=self.mcmc_samples,
                        warmup_steps=self.mcmc_warmup_samples,
                        num_chains=self.mcmc_chains,
                        initial_params=self.initial_params,
                    )

                self.mcmc_.run(X, y)
                return None
            case "vi":
                if self.svi_ is None:  #  allows to provide a user defined SVI instance, too.
                    self.svi_ = pyro.infer.SVI(self._pyro_model, self._guide, self._optim, self._loss)
                self.losses_ = []
                for i in range(self.vi_iter):
                    loss = self.svi_.step(X, y)
                    self.losses_.append(loss)
                    if i % 100 == 0:
                        logger.debug(f"[SVI] loss {i:4d}: {loss:.4f}")
                return self.losses_
            case _:
                raise NotImplementedError(
                    f"inference_method_name '{self.inference_method_name}' not implemented. Valid inference_method_name: 'mcmc', 'vi'."
                )

    def predict(
        self,
        X: torch.Tensor | None,
        n_predictive_samples=500,
        sample_prior=False,
        parallel=False,
    ) -> dict[str, torch.Tensor]:
        """Generates predictive samples from the fitted posterior or the unconditioned prior distribution.

        Args:
            X (torch.Tensor | None): The input feature data of shape (batch, features) for which to generate predictions.
            n_predictive_samples (int, optional): The number of predictive samples to draw. Defaults to 500.
            sample_prior (bool, optional): If True, draws samples from the prior instead of the fitted posterior. Defaults to False.
            parallel (bool, optional): If True, vectorize the model and evaluate the posterior samples in parallel. Defaults to False.

        Returns:
            dict: A dictionary containing the predictive samples generated by the underlying Pyro model for each latent parameter.
        """
        assert self.mcmc_ is not None or self.svi_ is not None and "Regressor not trained. Run fit() first."
        if X is not None:
            assert X.dim() == 2 and "X shape must be (batch, features)"

        if sample_prior:
            predictive = Predictive(
                self._pyro_model,
                posterior_samples={},
                num_samples=n_predictive_samples,
                parallel=parallel,
            )
        else:
            if self.mcmc_ is not None:
                predictive = Predictive(
                    self._pyro_model,
                    posterior_samples=select_samples(self.mcmc_.get_samples(), n_predictive_samples),
                    parallel=parallel,
                )
            else:
                predictive = Predictive(
                    self._pyro_model,
                    guide=self._guide,
                    parallel=parallel,
                    num_samples=n_predictive_samples,
                )
        return predictive(X)

    def inference_diagnostics(self, print_summary=True) -> dict:
        """Computes and optionally prints diagnostic of the inference run.

        Args:
            print_summary (bool, optional): Whether to print the MCMC summary table to the console. Defaults to True.

        Returns:
            dict: A dictionary containing diagnostic metrics (like effective sample size and Gelman-Rubin statistics for MCMC, and the losses for VI).
        """
        if self.mcmc_ is not None:
            if print_summary:
                self.mcmc_.summary()
            return self.mcmc_.diagnostics()
        else:
            return {"loss": self.losses_}

    def score(self, X, y=None):
        raise NotImplementedError("score() method not implemented")

    def get_posterior(self) -> az.InferenceData | torch.distributions.Distribution:
        """If MCMC, extracts the posterior samples as an ArviZ InferenceData object for advanced analysis and plotting.
        If VI, return the variational distribution.

        Returns:
            arviz.InferenceData | torch.distributions.Distribution: The posterior distribution.
        """
        if self.mcmc_ is not None:
            try:
                return az.from_pyro(self.mcmc_)
            except KeyError as e:  # Automatic RandomWalk kernel fails, construct the arviz object manually.
                samples = self.mcmc_.get_samples(group_by_chain=True)
                posterior = {k: v.detach().cpu().numpy() for k, v in samples.items()}
                return az.from_dict(posterior=posterior)
        return self._guide.get_posterior()

    def load_posterior_arviz(self, idata: az.InferenceData):
        """Set the samples of the internal mcmc object to the given one. This allows to use the predict() method without calling fit() first.

        Args:
            idata (az.InferenceData): The posterior data.
        """
        if self.mcmc_ is None:
            self.mcmc_ = MCMC(
                self._kernel,
                num_samples=self.mcmc_samples,
                warmup_steps=self.mcmc_warmup_samples,
                num_chains=self.mcmc_chains,
                initial_params=self.initial_params,
            )
            self._setup_mcmc()
        posterior = {var: torch.tensor(idata.posterior[var].values) for var in idata.posterior.data_vars}
        self.mcmc_._samples = posterior

    def render_model(self, x_dummy, filename=None):
        """Renders a graphical representation of the Pyro probabilistic model.

        Args:
            x_dummy (torch.Tensor): A dummy input tensor used to trace the model's execution graph.
            filename (str | None, optional): The file path to save the rendered graph (e.g., 'model.png'). Defaults to None.
        """
        pyro.render_model(self._pyro_model, (x_dummy,), filename=filename)
