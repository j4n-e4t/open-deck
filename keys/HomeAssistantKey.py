import requests
from keys.Key import Key

class HomeAssistantKey(Key):
    provider = None
    def __init__(
        self,
        key_config: dict,
        stream_deck,
        provider,
    ):
        super().__init__(key_config, stream_deck)
        self.provider = provider

    def action(self) -> None:
        self.provider.send(
            self.action_data["domain"],
            self.action_data["action"],
            self.action_data["entity"],
        )
    
