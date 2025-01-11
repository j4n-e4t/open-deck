from keys.Key import Key


class JumpKey(Key):
    def __init__(self, key_config: dict, stream_deck):
        super().__init__(key_config, stream_deck)

    def action(self) -> int:
        return self.action_data["page"]

    def __str__(self):
        return f"ScriptKey(key_id={self.key_id}, label={self.label}, icon={self.icon}, script={self.action_data['script']})"
