import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper
from keys.Key import Key
from config import config


class ClockKey(Key):
    def __init__(self, key_config: dict, stream_deck):
        super().__init__(key_config, stream_deck)
        self.last_update = 0
        self.update_interval = 1
        self.key_config = key_config

    def action(self) -> None:
        pass

    def set_image(self):
        image = PILHelper.create_scaled_key_image(
            self.stream_deck, Image.new("RGB", (72, 72), "black"), margins=[0, 0, 0, 0]
        )

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(
            config["font_dir"] + "/" + config["stream_deck"]["font"]["style"] + ".ttf",
            20,
        )

        current_time = datetime.now().strftime("%H:%M")
        draw.text(
            (image.width / 2, image.height / 2),
            text=current_time,
            font=font,
            anchor="mm",
            fill=(config["stream_deck"]["font"]["color"]),
        )

        sd_image = PILHelper.to_native_key_format(self.stream_deck, image)
        self.stream_deck.set_key_image(self.key_id, sd_image)
        self.last_update = time.time()

    def update(self):
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self.set_image()
