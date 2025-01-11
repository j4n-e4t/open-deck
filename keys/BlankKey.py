from keys.Key import Key


class BlankKey(Key):
    def __init__(self, key_config: dict, stream_deck):
        super().__init__(key_config, stream_deck)

    def action(self) -> None:
        pass

    def __str__(self):
        return f"BlankKey(key_id={self.key_id}, label={self.label}, icon={self.icon})"

    def set_image(self):
        self.stream_deck.set_key_image(self.key_id, None)
