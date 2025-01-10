import yaml
from schema import Schema, Optional
from StreamDeck.DeviceManager import DeviceManager
from keys.Key import Key
from keys.ScriptKey import ScriptKey
from keys.AppleMusicKey import AppleMusicKey
from keys.HomeAssistantKey import HomeAssistantKey
from keys.ApplicationKey import ApplicationKey
from keys.ClockKey import ClockKey
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper
import signal
import sys
import time
from config import config


def render_key(key_config: dict, stream_deck) -> Key:
    match key_config["type"]:
        case "script":
            return ScriptKey(key_config, stream_deck)
        case "apple_music":
            return AppleMusicKey(key_config, stream_deck)
        case "home_assistant":
            return HomeAssistantKey(
                key_config,
                config["homeassistant"]["url"],
                config["homeassistant"]["token"],
                stream_deck,
            )
        case "application":
            return ApplicationKey(key_config, stream_deck)
        case "clock":
            return ClockKey(key_config, stream_deck)
        case _:
            raise ValueError(f"Invalid key type: {key_config['type']}")


def key_change_callback(stream_deck, key_id: int, state: bool):
    if state and key_id in keys:
        keys[key_id].action()
        if keys[key_id].key_config["type"] == "apple_music":
            keys[key_id].set_image()


def signal_handler(sig, frame):
    print("\nClosing Stream Deck...")

    stream_deck.reset()
    stream_deck.close()

    sys.exit(0)


def main():
    stream_decks = DeviceManager().enumerate()
    if len(stream_decks) == 0:
        print("No stream decks found")
        return

    signal.signal(signal.SIGINT, signal_handler)

    global stream_deck
    stream_deck = stream_decks[0]

    if not stream_deck.is_visual():
        print("Stream deck is not visual")
        return

    stream_deck.open()

    global keys
    keys = {}

    for key_config in config["keys"]:
        key = render_key(key_config, stream_deck)
        keys[key_config["key_id"]] = key

    print(
        "Opened '{}' device (serial number: '{}')".format(
            stream_deck.deck_type(), stream_deck.get_serial_number()
        )
    )
    stream_deck.reset()
    stream_deck.set_brightness(config["stream_deck"]["brightness"])

    for key in keys.values():
        key.set_image()

    stream_deck.set_key_callback(key_change_callback)

    try:
        print("Press Ctrl+C to exit...")
        while True:
            # Update all keys that need periodic updates
            for key in keys.values():
                if hasattr(key, "update"):
                    key.update()
            time.sleep(0.1)  # Small sleep to prevent high CPU usage
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()
