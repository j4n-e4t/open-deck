from keys.ScriptKey import ScriptKey
from keys.JumpKey import JumpKey
from keys.AppleMusicKey import AppleMusicKey
from keys.HomeAssistantKey import HomeAssistantKey
from keys.ApplicationKey import ApplicationKey
from keys.ClockKey import ClockKey
from keys.BlankKey import BlankKey
from keys.Key import Key


class KeyRenderer:
    def __init__(self, stream_deck, providers: dict):
        self.stream_deck = stream_deck
        self.providers = providers

    def key(self, key_config: dict) -> Key:
        key = None
        match key_config["type"]:
            case "script":
                key = ScriptKey(key_config, self.stream_deck)
            case "apple_music":
                key = AppleMusicKey(
                    key_config, self.stream_deck, self.providers["apple_music"]
                )
            case "home_assistant":
                key = HomeAssistantKey(
                    key_config,
                    self.stream_deck,
                    self.providers["homeassistant"],
                )
            case "application":
                key = ApplicationKey(
                    key_config, self.stream_deck, self.providers["application"]
                )
            case "clock":
                key = ClockKey(key_config, self.stream_deck)
            case "jump":
                key = JumpKey(key_config, self.stream_deck)
            case "blank":
                key = BlankKey(key_config, self.stream_deck)
            case _:
                raise ValueError(f"Invalid key type: {key_config['type']}")

        key.set_image()
        return key
