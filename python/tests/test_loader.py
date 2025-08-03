import pytest
from pyconfigloader import ConfigLoader

class MyAppConfigLoader(ConfigLoader):
    def __init__(self, config_path):
        super().__init__(config_path)

    def validate(self, config: dict):
        if "app_host" not in config:
            raise Exception("'app_host' field should be provided in config")
        if "app_port" not in config:
            raise Exception("'app_port' field should be provided in config")

@pytest.mark.parametrize(
        "file_path", ["./config.yaml", "./config.json"]
)
def test_load_config(monkeypatch, file_path):
    monkeypatch.setenv("APP_ONLINE", "false")
    monkeypatch.setenv("VARIABLE", "value")
    monkeypatch.setenv("ID", "1")
    monkeypatch.setenv("APP_OTHER_PARAM", "param_${VARIABLE}_${ID}")

    config_loader = MyAppConfigLoader(file_path)
    config = config_loader.load_config()

    # validate config
    config_loader.validate(config)

    # assertions
    assert config["app_host"] == "127.0.0.1"
    assert config["app_port"] == 8080
    assert not config["app_online"]
    assert config["app_other_param"] == "param_value_1"
