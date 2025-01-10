import subprocess
from keys.Key import Key


class ApplicationKey(Key):
    def __init__(self, key_config: dict, stream_deck):
        super().__init__(key_config, stream_deck)
        self.application_name = key_config["action_data"]["application"]

    def action(self) -> None:
        print(f"Launching application {self.application_name}")
        subprocess.run(
            [
                "osascript",
                "-e",
                f'tell application "{self.application_name}" to activate',
            ]
        )
