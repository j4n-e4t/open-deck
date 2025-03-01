from keys.Key import Key


class ApplicationKey(Key):
    def __init__(self, key_config: dict, stream_deck, provider):
        super().__init__(key_config, stream_deck)
        self.application_name = key_config["action_data"]["application"]
        self.provider = provider

    def action(self) -> None:
        self.provider.launch(self.application_name)
