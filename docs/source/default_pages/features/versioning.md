# versioning
**Reproducibility** is crucial in science.
While in probabilistic modeling sampled results may vary it is even more desireable to know exactly which code produced which result.
Versioning approach in this template aims to have code (+ outcome/results and visualisations, which may be published) and documentation in sync and uniquely identifiable.

Therefore, this template utilizes the package [setuptools_scm](https://setuptools-scm.readthedocs.io/en/latest/) to achieve that.
It basically uses git (or other scm) information to derive a version number from that.

While working on a project, one could always simply use

```python
from equayes import version
```
which produces a version string like `'0.3.dev2+gd04a1f4.d20240116'` which is defined to follow the schema:  
`<latest_version_tag + 1>.dev<commits_since_latest_version_tag>+<commit_id>.<date_information>`
