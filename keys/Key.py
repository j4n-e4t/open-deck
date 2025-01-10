from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper
from config import config


class Key:
    def __init__(self, key_config: dict, stream_deck):
        self.key_id = key_config["key_id"]
        self.label = key_config["label"] if "label" in key_config else ""
        self.type = key_config["type"]
        self.action_data = (
            key_config["action_data"] if "action_data" in key_config else {}
        )
        self.key_config = key_config
        self.stream_deck = stream_deck

    def __str__(self) -> str:
        return f"Key(key_id={self.key_id}, label={self.label}, icon={self.key_config['icon'] if 'icon' in self.key_config else ''}, type={self.type})"

    def set_image(self):
        icon = Image.open(
            config["icon_dir"] + "/" + self.key_config["icon"]
            if "icon" in self.key_config
            else ""
        )

        image = PILHelper.create_scaled_key_image(
            self.stream_deck,
            icon,
            margins=[
                config["stream_deck"]["key_margin"],
                config["stream_deck"]["key_margin"],
                20 if self.label else config["stream_deck"]["key_margin"],
                config["stream_deck"]["key_margin"],
            ],
        )

        if self.label:
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(
                config["font_dir"]
                + "/"
                + config["stream_deck"]["font"]["style"]
                + ".ttf",
                config["stream_deck"]["font"]["size"],
            )
            draw.text(
                (image.width / 2, image.height - 5),
                text=self.label,
                font=font,
                anchor="ms",
                fill=config["stream_deck"]["font"]["color"],
            )

        sd_image = PILHelper.to_native_key_format(self.stream_deck, image)
        self.stream_deck.set_key_image(self.key_id, sd_image)
