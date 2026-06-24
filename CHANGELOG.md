# Changelog

All notable changes to this project will be documented in this file. See examples below.

## [Unreleased]

### Added

- New feature or enhancement description.

### Changed

- Description of changes to existing functionality.

### Fixed

- Bug fixes and other corrections.

### Removed

- Features or functionality that have been removed.

### Known/potential issues

- Add known issues of this version (that are not fixed).

## [1.2.0] - 2026-05-11 - Update ArviZ to v1.+

### Changed

- Increase ArviZ Major version from 0.23. to 1.*
  - az.InferenceData is replaced by xarray.DataTree.

## [1.1.0] - 2026-05-11 - Add parameter 'latent_variables'

### Added

- Enables probabilistic treatment of sp.symbols in the passed sympy expression.
  - Symbols in the passed sympy expression can be treated as random variables by specifying them in the new 'latent_variables' parameter of sympy.

    ```python
    Equayes(
        lat0 + sin(3*x0), latent_variables=[lat0]
    )
    ```

- Add cantilever notebook
  - An example of a physical motivated problem (governing equation is known). The use of Equayes.latent_variables is demonstrated in the notebook.

### Known/potential issues

- ArviZ received a major update 0.23.4 $\rightarrow$ 1.0.0
  - This change introduces major API changes
  - Equayes relies on arviz 0.23 API

## [1.0.0] - 2026-03-19 - Initial Release

### Added

- Equation to pyro model
  - replace all float constants that are not in `skip` with normal distributions $\mathcal{N}(0, \sigma^2=1000)$
  - add Gaussian likelihod as final output layer $\mathcal{N}(y, \epsilon), \quad \epsilon \sim \text{HalfNormal}(1)$
  - latent parameters are numbered in order of appearance in the sympy string representation.
    - Note: The parameter order while defining the sympy equation has no effect, as sympy does not store this order.
- Inference methods MCMC and VI
  - MCMC: available kernels
    - NUTS
    - Random Walk
      - gradient free
      - no JIT-compilation supported in pyro
  - VI
    - AutoMultivariateNormal Guide over all latent sites
  - Inference initialization: Inference uses the original constants in the equation as starting points.
- JiT compilation
- Inference via `fit()`
- prior and posterior samples via `predict()`
- access to the posterior distribution as arviz InferenceData (MCMC) or torch distribution (VI) via `get_posterior()`
- `inference_diagnostics()` to get information on the inference run.
- `load_posterior_arviz()` to load an MCMC inference result
  - enables `predict()` without a prior call to `fit()`

### Known/potential issues

- ArviZ received a major update 0.23.4 $\rightarrow$ 1.0.0
  - This change introduces major API changes
  - Equayes relies on arviz 0.23 API
