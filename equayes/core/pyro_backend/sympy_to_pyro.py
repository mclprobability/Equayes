import pyro
import pyro.distributions as dist
import sympy as sp
import torch
from sympy.utilities.lambdify import lambdify


def create_pyro_model(sympy_expr: sp.Expr, x_symbols: list, theta_symbols: list, output_dim: int):
    """Creates a Pyro probabilistic model from a parameterized SymPy expression.

    Args:
        sympy_expr (sp.Expr): The parameterized SymPy expression representing the forward model.
        x_symbols (list): List of SymPy symbols representing the input features X.
        theta_symbols (list): List of SymPy symbols representing the learnable parameters theta.
        output_dim (int): The dimensionality of the output (number of target columns).

    Returns:
        callable: A probabilistic Pyro model function compatible with pyro.infer.
    """

    # 1. Compile SymPy expression to a PyTorch-compatible function
    # We combine arguments so the function signature is (*x_inputs, *theta_inputs)
    # 'modules=torch' ensures math operations (sin, exp, etc.) use torch equivalents
    torch_func = lambdify(x_symbols + theta_symbols, sympy_expr, modules="torch")

    def model(x_data: torch.Tensor | None, y_data: torch.Tensor | None = None):
        """
        The Pyro Model.
        x_data: Tensor of shape (Batch, features)
        y_data: Tensor of shape (Batch, output_dim) [Optional, for training]
        # ToDo: if all broadcasting is correct needs to be evaluated
        """

        N = (
            y_data.shape[0] if y_data is not None else 1
        )  # during inference, y must be given and y_data.shape[0] ==  x_data.shape[0] if x_data is not None
        N = x_data.shape[0] if x_data is not None else N  # for Predictive samples, y is None, but x_data can be given
        # 2. Sample Theta (Priors)
        # User Constraint: theta_i ~ N(0, 1000)
        # Note: Normal(loc, scale). Variance=1000 implies scale=sqrt(1000) ≈ 31.62
        theta_samples = []
        theta_scale = torch.tensor(31.62)

        for i, sym in enumerate(theta_symbols):
            t_val = pyro.sample(
                f"theta_{sym.name}", dist.Normal(0.0, theta_scale).expand([1]).to_event(1)
            )  # shape (1,) or (particles,)
            if t_val.shape != () and t_val.shape[0] > 1:
                t_val = t_val.view(-1, 1, 1)
            else:
                t_val = t_val.view(-1, 1)
            theta_samples.append(t_val)

        # 3. Sample Epsilon (Noise Sigma)
        # We assume independent noise per output dimension M.
        # We use a HalfNormal prior to ensure positivity.
        # todo: Remark, if the functions output is 1d, but output_dim > 1, the resulting output dim of the model is output-dim. If this is beneficial or creates confusion (i.e. an exception would be appropriate) needs to be discussed
        epsilon = pyro.sample("epsilon", dist.HalfNormal(1.0).expand([output_dim]).to_event(1))  # shape (1,) or (particles,1)
        if epsilon.shape != () and epsilon.shape[0] > 1:
            epsilon = epsilon.view(-1, 1, 1)
        else:
            epsilon = epsilon.view(-1, 1)
        # We split x_data into columns to feed into the lambdified function
        # x_args will be a list of (N,1)) tensors
        if x_data is not None:
            x_args = [x_data[:, None, i] for i in range(len(x_symbols))]
        else:
            x_args = []
        # todo: If M>1, sympy returns (N, M) usually via torch.stack inside lambdify.
        mu = torch_func(*x_args, *theta_samples)  # shape (scalar or Batch, or (Batch, M))
        if mu.dim() < 2:
            mu = torch.atleast_1d(mu).unsqueeze(-1).expand((N, output_dim))  # ensure shape: (Batch,M)
        mu = pyro.deterministic("mu", mu)

        with pyro.plate("obs_plate", N, dim=-1):
            return pyro.sample("obs", dist.Normal(mu, epsilon).to_event(1), obs=y_data)

    return model
