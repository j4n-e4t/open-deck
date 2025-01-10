import subprocess
from keys.Key import Key
from config import config


class ScriptKey(Key):
    def __init__(self, key_config: dict, stream_deck):
        super().__init__(key_config, stream_deck)

    def action(self) -> None:
        print(f"Running script {self.action_data['script']}")
        subprocess.run(
            ["bash", "-c", f"{config['script_dir']}/{self.action_data['script']}"]
        )

    def __str__(self):
        return f"ScriptKey(key_id={self.key_id}, label={self.label}, icon={self.icon}, script={self.action_data['script']})"
