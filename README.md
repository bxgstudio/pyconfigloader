# PyConfigLoader
<img src="./assets/CL.png" alt="Texte alternatif" width="200"/>
<br/>
This repository is the python implementation of ConfigLoader, a project that that provides a simple way to load application configuration from file and to override parameters with associated env vars if any.
An evaluate of env vars is done after configuration loading which allows you to customize properly environment variables on tricky scenarii (can happen in k8s contexts to concatenate variables from POD_NAME and add a suffix for example).

Here you can find the golang version of this project: [Golang repository](https://github.com/bxgstudio/goconfigloader)

---

Manage following configuration file formats: 
- yaml
- json

---

Manage following types of env vars:
- ENV=string
- ENV=${OTHER_ENV}_{ANOTHER_ONE}_string

---

# Installation

pip install appconfigloader

# Mechanism

To use this package, you need to implement a derived class from ``ConfigLoader``. This constraint is here to force the product that uses this package to do a logical check of loaded config in order to build robust code by implementing the function ``validate``.

Types that are manage are the following:
- int
- string
- bool

If a field is named ``application_host`` in provided configuration file and that there is an environment variable named ``APPLICATION_HOST``, the environment variable will override the field provided in configuration file.

If an environement variable is composed by other variable, the subset of variables included in the environment variable will be interpreted. Example:
```
config file (yaml):
name: my_name
id: 2
other_variable: "random_name"

environement variables:
NAME=doe
ID=1
OTHER_VARIABLE=prefix_${NAME}_${ID}

result after using appconfigloader:
{
    "name": "doe",
    "id": 1,
    "other_variable": "prefix_doe_1"
}
```

# Usage

```python
from appconfigloader import ConfigLoader

class MyAppConfigLoader(ConfigLoader):
    def __init__(self, config_path):
        super().__init__(config_path)

    def validate(self, config: dict):
        if "app_host" not in config:
            raise Exception("'app_host' field should be provided in config")
        if "app_port" not in config:
            raise Exception("'app_port' field should be provided in config")

if __name__ == "__main__":
    # Init
    config_loader = MyAppConfigLoader("/path/to/config/file.yaml")

    # Load config in dict
    config = config_loader.load_config()

    # Validate configuration
    config_loader.validate(config)

    # ...
```

a full example is available in tests/test_loader.py.

# Authors

- Etienne Galecki - [@galecki](https://github.com/egck)
- Antoine Breton - [@breton](https://github.com/antbreton)