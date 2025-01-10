import yaml
from schema import Schema, Optional

CONFIG_PATH = "/Users/julian/.config/open-deck/config.yaml"

config_schema = Schema(
    {
        "icon_dir": str,
        "font_dir": str,
        "script_dir": str,
        "stream_deck": Schema(
            {
                "brightness": int,
                "key_margin": int,
                "font": Schema(
                    {
                        "size": int,
                        "style": str,
                        "color": str,
                    }
                ),
            }
        ),
        Optional("homeassistant"): Schema(
            {
                "url": str,
                "token": str,
            }
        ),
        "keys": [
            Schema(
                {
                    "key_id": int,
                    Optional("label"): str,
                    "type": str,
                    Optional("action_data"): dict,
                    Optional("icon"): str,
                }
            )
        ],
    }
)


def load_config(config_path: str) -> dict:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    if not config_schema.validate(config):
        raise ValueError("Invalid config")
    return config


config = load_config(CONFIG_PATH)
