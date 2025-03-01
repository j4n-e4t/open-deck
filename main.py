from StreamDeck.DeviceManager import DeviceManager
from key_renderer import KeyRenderer
import signal
import sys
import time
from config import config
from keys.JumpKey import JumpKey

current_keys = {}


def signal_handler(sig, frame):
    print("\nClosing Stream Deck...")

    stream_deck.reset()
    stream_deck.close()

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

    global renderer
    renderer = KeyRenderer(stream_deck)

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
