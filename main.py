from StreamDeck.DeviceManager import DeviceManager
from key_renderer import KeyRenderer
import signal
import sys
import time
from config import config
from keys.JumpKey import JumpKey
from providers.HomeAssistantProvider import HomeAssistantProvider
from providers.AppleMusicProvider import AppleMusicProvider
from providers.MacOSApplicationProvider import MacOSApplicationProvider

current_keys = {}
providers = {
    "homeassistant": None,
    "apple_music": None,
    "application": None,
}


def initialize_providers():
    for provider in providers.keys():
        match provider:
            case "homeassistant":
                providers["homeassistant"] = HomeAssistantProvider(
                    config["homeassistant"]["url"], config["homeassistant"]["token"]
                )
                providers["homeassistant"].connect()
            case "apple_music":
                providers["apple_music"] = AppleMusicProvider()
            case "application":
                providers["application"] = MacOSApplicationProvider()
            case _:
                pass


def signal_handler(sig, frame):
    print("\nClosing Stream Deck...")

    stream_deck.reset()
    stream_deck.close()

    for provider in providers.values():
        if provider is not None and hasattr(provider, "close"):
            provider.close()

    sys.exit(0)


def handle_key_press(deck, key_id: int, state: bool):
    if state and key_id in current_keys:
        if isinstance(current_keys[key_id], JumpKey):
            open_page(current_keys[key_id].action())
        else:
            current_keys[key_id].action()


def open_page(page_id: int):
    current_keys.clear()
    for key_config in config["pages"][page_id]["keys"]:
        current_keys[key_config["key_id"]] = renderer.key(key_config)


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
    stream_deck.reset()

    initialize_providers()
    global renderer
    renderer = KeyRenderer(stream_deck, providers)

    current_page = config["home_page"]

    open_page(current_page)

    stream_deck.set_key_callback(handle_key_press)

    print(
        "Connected to '{}' device (serial number: '{}')".format(
            stream_deck.deck_type(), stream_deck.get_serial_number()
        )
    )
    stream_deck.set_brightness(config["stream_deck"]["brightness"])

    try:
        print("Press Ctrl+C to exit...")
        while True:
            for key in list(current_keys.values()):
                if hasattr(key, "update"):
                    key.update()
            time.sleep(0.2)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()
