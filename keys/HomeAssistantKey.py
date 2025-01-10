import requests
from keys.Key import Key


class HomeAssistantKey(Key):
    def __init__(
        self,
        key_config: dict,
        homeassistant_url: str,
        homeassistant_token: str,
        stream_deck,
    ):
        super().__init__(key_config, stream_deck)
        self.homeassistant_url = homeassistant_url
        self.homeassistant_token = homeassistant_token

    def action(self) -> None:
        response = requests.post(
            self.homeassistant_url
            + "/api/services/"
            + self.action_data["domain"]
            + "/"
            + self.action_data["action"],
            headers={"Authorization": "Bearer " + self.homeassistant_token},
            json={"entity_id": self.action_data["entity"]},
        )
        if response.status_code != 200:
            raise ValueError(
                f"Failed to call Home Assistant API: {response.status_code}"
            )

        print(f"Successfully called Home Assistant API: {response.status_code}")
