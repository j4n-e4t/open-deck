import yaml
from schema import Schema, Optional, SchemaError

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
        "home_page": int,
        "pages": [
            Schema(
                {
                    "page_id": int,
                    "keys": [
                        Schema(
                            {
                                "key_id": int,
                                Optional("label"): str,
                                "type": str,
                                Optional("action_data"): {
                                    Optional("page"): int,
                                    Optional("application"): str,
                                    Optional("domain"): str,
                                    Optional("action"): str,
                                    Optional("entity"): str,
                                    Optional("play_icon"): str,
                                    Optional("pause_icon"): str,
                                    Optional("script"): str,
                                },
                                Optional("icon"): str,
                            }
                        )
                    ],
                }
            )
        ],
    }
)


def load_config(config_path: str) -> dict:
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    try:
        validated_config = config_schema.validate(config)
        return validated_config
    except SchemaError as e:
        raise ValueError(f"Invalid config: {e}")


config = load_config(CONFIG_PATH)
