# config folder

This folder provides a place to define all your project configuration.  
It supports YAML configuration and aims to make it easy for you to implement clear **code <> config separation**.  

From `equayes.utils` you can import `CONFIG`, `CONSTANTS`, and `PARAMETERS` as dictionary into your code base.  

- `CONFIG` stores all the key/value pairs from the `globals.yml` file(s)
- `CONSTANTS` are just a subset of `CONFIG` under the level *constants* in that file (for convinience)
- `PARAMETERS` dictionary stores configuration key/values pairs defined in `parameters.yml` file(s)


## base vs. local folder

1. **same named files are merged**  
    - configurations from the files `globals.yml` in base and local folder are merged
    - same with config from `parameters.yml` files

2. **local folder configs takes precedence**  
    - if the key is identical, the local value takes precedence over base value
    - identical means same named file, same key and same hierarchy/nesting
3. **local folder is `.gitignore`d**  
so e.g. sensitive or device-based configuration should be defined in local config while the base folder is meant to land on GitHub.

## example
Note:
Changes in your config require a kernel reload to be importable via:

```python
from equayes.utils import CONFIG, CONSTANTS, PARAMETERS
```

or you load them directly via:

```python
# how to load config files manually:
my_config = load_yaml_config(configfile="base/globals.yml") # loads globals.yml file from base folder
update_yaml_config(base_dict=my_config, configfile="local/globals.yml") # updates "my_config" dictionary with globals.yml from local folder

# now the "my_config" dictionary stores all information defined in `equayes/config/base/globals.yaml` and `_/local/globals.yml`.
# identical configuration keys in `_/local/globals.yml` take precedence.
```