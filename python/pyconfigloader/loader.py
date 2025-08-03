import os
import re
import json
import yaml
from abc import ABC, abstractmethod


class ConfigLoader(ABC):
    def __init__(self, config_path: str):
        self.config_path = config_path

    @abstractmethod
    def validate(self, config: dict):
        """
        Method to be implemented to check if the configuration is according to what application expects.
        """
        pass

    def load_config(self) -> dict:
        """
        Try to load a yaml or json configuration file.
        override configuration file fields with env vars if found.
        """
        # try to open file
        try:
            config_file = open(self.config_path, "r", encoding="utf-8")
        except FileNotFoundError as exc:
            raise Exception(f"configuration file not found at path: {self.config_path}") from exc

        # try to load file as yaml first
        try:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
        # if exception here, try to open file as json
        except Exception as exc:
            try:
                config = json.load(config_file)
            except Exception as exc:
                raise Exception(f"configuration file is none of yaml or json") from exc
        finally:
            config_file.close()

        # Override configuration fields with associated env vars if any
        for key in config:
            # Extract env var if defined
            env_var_value = os.getenv(key.upper(), None)

            # cas found env vars in good type
            if env_var_value:

                # Parse integer
                if env_var_value.isdigit():
                    config[key] = int(env_var_value)

                # Parse bool
                elif env_var_value.lower() == "true":
                    config[key] = True
                elif env_var_value.lower() == "false":
                    config[key] = False

                # Parse string
                else:
                    config[key] = self._evaluate_vars(env_var_value)

        return config
    
    def _evaluate_vars(self, envvar: str) -> str:
        # detect variable string in env var input
        # example: ENVVAR=my_param_${POD_IP}_${POD_NAME}
        variable_regexp = re.compile(r"\$\{([a-zA-Z0-9_-]+)\}")

        while True:
            # Search match in provided envvar
            match = variable_regexp.search(envvar)

            # Return when no match found
            if not match:
                return envvar

            # extract first match and replace if with desired envvar
            # example: 
            # POD_IP=192.168.1.2
            # ENVVAR=my_param_${POD_IP}_${POD_NAME} --> my_param_192.168.1.2_${POD_NAME}
            var_name = match.group(1)
            env_value = os.getenv(var_name, "")
            envvar = envvar.replace(f"${{{var_name}}}", env_value, 1)