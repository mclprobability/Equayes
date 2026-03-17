import arviz as az
import numpy as np
import pyro
import torch
from pyro.infer import Predictive

from equayes.utils import log

logger = log.getLogger("Pyro Utils")


def get_initial_param_dict(exp_param_values: dict, n_chains, param_prefix="theta_") -> dict[str, torch.Tensor]:
    """Generates initial parameter tensors for the MCMC chains.

    Args:
        exp_param_values (dict): A mapping of parameter names to their initial extracted numeric values.
        n_chains (int): The number of MCMC chains being initialized.
        param_prefix (str, optional): The string prefix used for naming the parameters. Defaults to "theta_".

    Returns:
        dict: A dictionary containing the initialized PyTorch tensors, duplicated across the specified number of chains.
    """
    initial_params = {
        f"{param_prefix}{k}": (torch.tensor([float(v)]).repeat((n_chains, 1)) if n_chains > 1 else torch.tensor([float(v)]))
        for k, v in exp_param_values.items()
    }
    initial_params["epsilon"] = (
        torch.tensor([float(1e-2)]).repeat((n_chains, 1)) if n_chains > 1 else torch.tensor([float(1e-2)])
    )
    return initial_params


def guide_to_inference_data(model, guide, *args, num_samples=3000, parallel=True, **kwargs):
    """
    Converts a trained Pyro SVI guide into an ArviZ InferenceData object.

    Args:
        model: The Pyro model.
        guide: The trained Pyro guide.
        *args, **kwargs: The arguments passed to the model/guide during inference.
        num_samples: Number of draws to take from the guide.
    """
    predictive = Predictive(model, guide=guide, num_samples=num_samples, parallel=parallel)
    samples = predictive(*args, **kwargs)

    # 2. Inspect the model trace to separate latents from observables
    trace = pyro.poutine.trace(model).get_trace(*args, **kwargs)
    latent_sites = [name for name, node in trace.nodes.items() if node["type"] == "sample" and not node["is_observed"]]
    observed_sites = [name for name, node in trace.nodes.items() if node["type"] == "sample" and node["is_observed"]]

    # 3. Format dictionaries for ArviZ (ArviZ expects shape: [chains, draws, *shape])
    # Since SVI doesn't have "chains", we add a single dummy chain dimension.
    posterior_dict = {}
    for site in latent_sites:
        if site in samples:
            val = samples[site].detach().cpu().numpy()
            posterior_dict[site] = np.expand_dims(val, axis=0)  # Shape: (1, num_samples, ...)

    posterior_predictive_dict = {}
    for site in observed_sites:
        if site in samples:
            val = samples[site].detach().cpu().numpy()
            posterior_predictive_dict[site] = np.expand_dims(val, axis=0)

    # 4. Extract the actual observed data from the trace
    observed_data_dict = {}
    for site in observed_sites:
        val = trace.nodes[site]["value"].detach().cpu().numpy()
        observed_data_dict[site] = val

    # 5. Compile into ArviZ InferenceData
    idata = az.from_dict(
        posterior=posterior_dict,
        posterior_predictive=posterior_predictive_dict,
        observed_data=observed_data_dict,
    )

    return idata
