import time
from PIL import Image, ImageDraw, ImageFont
from keys.Key import Key
from config import config
from StreamDeck.ImageHelpers import PILHelper


class AppleMusicKey(Key):
    def __init__(self, key_config: dict, stream_deck, provider):
        self.provider = provider
        self.last_update = None
        if key_config["action_data"]["action"] == "play/pause":
            self.key_config = key_config
            self.key_config["icon"] = "play.png"
        super().__init__(key_config, stream_deck)

    def action(self) -> None:
        match self.action_data["action"]:
            case "play/pause":
                self.provider.play_pause()
            case "next":
                self.provider.next()
            case "previous":
                self.provider.previous()
            case _:
                raise ValueError(f"Invalid action: {self.action_data['action']}")
        self.set_image()

    def set_image(self):
        self.last_update = time.time()
        if self.action_data["action"] == "play/pause":
            icon = Image.open(
                config["icon_dir"] + "/" + self.key_config["action_data"]["pause_icon"]
                if self.provider.is_playing()
                else config["icon_dir"]
                + "/"
                + self.key_config["action_data"]["play_icon"]
            )
        else:
            icon = Image.open(config["icon_dir"] + "/" + self.key_config["icon"])

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

    def update(self):
        if (
            self.action_data["action"] == "play/pause"
            and time.time() - self.last_update > 1
        ):
            self.set_image()
