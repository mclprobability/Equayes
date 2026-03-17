# Configuration

**Separating configuration from code** is a highly encouraged software development best practice.  
This template supports a developer to achieve that goal by
- providing dedicated locoations to define configs
- implementing loading functions to easily use config within code (python)

```{margin}
```{admonition} config is in source code folder
Putting the config folder inside the `<package_name>` source code folder was **not** the most intuitive decision.  
**Idea for a future release:**  
It might be a better choice to put it into the top-level folder, include it for python packaging and adapt config loading implementations.
```

## where to define config?
The dedicated config folder is placed here:

**`<Your_Repository>\   `> &nbsp; your repository root**\
`├── `**`<package_name>\   `> &nbsp; source code folder**\
`│   ├── `**`config\   `> &nbsp; put all your configuration & parameters here**; always separate configuration from code!\
`│   │   ├── `**`base\   `> &nbsp; define global configuration here**; it will land on git\
`│   │   │   ├── globals.yml   `> &nbsp; define "global" configurations like **paths** or **constants** here,\
`│   │   │   │                 `> &nbsp; use it in code with `<package_name>.CONFIG`\
`│   │   │   ├── parameters.yml   `> &nbsp; define parameters here, available in code with `<package_name>.PARAMETERS`\
`│   │   │   └── logging_config.yml   `> &nbsp; boilerplate configuration for the python logging implementation\
`│   │   └── `**`local\   `> &nbsp; define local configuration here (folder is .gitignored), identical config (to base config) is prioritized from here**\
`│   │       └── globals.yml   `> &nbsp; config here extends base/globals.yml, identical keys overwrite the base config\
`.   .`\
`.   .`

Use yaml syntax to define key:value pairs and their hierarchy. You can also define lists. Check out this [yaml cheat sheet](https://codebeautify.org/yaml-cheat-sheet) for more information.  

## how to use config in python?
If installed your package correctly, you can use config like this:

::::{tab-set}
:::{tab-item} global config
```{code-block} python
from equayes import CONFIG

print(CONFIG)
```
which results in a `dict` of all configuration placed in `globals.yml` file inside `base` **and** `local` folder (remember: local is gitignored and overwrites base if keys have identical names and hierarchy).
:::

:::{tab-item} parameters config
```python
from equayes import PARAMETERS

print(PARAMETERS)
```
which results in a `dict` of all configuration placed in `parameters.yml` file inside `base` **and** `local` folder (remember: local is gitignored and overwrites base if keys have identical names and hierarchy).
:::

:::{tab-item} constants
```python
from equayes import CONSTANTS

print(CONSTANTS)
```
This dictionary is simply a **subset** of `globals.yml` under the `constants` key.
:::
::::

```{admonition} Want to add other files?
:class: tip, dropdown
The package variables `CONFIG`, `PARAMETERS` & `CONSTANTS` are set in `equayes/utils/__init__.py` (and propagated to `equayes/__init__.py`).  

Look there to see how the constant variables are read and use the same pattern to provide additional config files/keys to your package globally.
```

### manually (re-)load
The initialisation of the configs uses the functions `load_yaml_config()` and `update_yaml_config` which are stored in `equayes/utils/configuration.py`.

If you want to reload configuration (because it has changed since last python kernel start), you can load the yaml config files locally again with:
```{code-block} python
my_config:dict = load_yaml_config(configfile="base/globals.yml")
update_yaml_config(base_dict=CONFIG, configfile="local/globals.yml")
# my_config is only available in local namespace!
```

If you want to reload the global variables defined in `equayes/__init__.py` (namely  `CONFIG`, `PARAMETERS` & `CONSTANTS`) in an **ipython environment** currently you have to restart your python kernel (unfortunately).

```{note} autoreload ipython magic
`%load_ext autoreload` + `%autoreload 2` does detect any changes in your package code (each .py file) and you can re-import packages/modules/functions/variables again without the need to restart your current kernel.  
**Unfortunately this does not work if you only change configs in your yaml file!**
```
