import subprocess

from PIL import Image, ImageDraw, ImageFont
from keys.Key import Key
from config import config
from StreamDeck.ImageHelpers import PILHelper


class AppleMusicKey(Key):
    def __init__(self, key_config: dict, stream_deck):
        if key_config["action_data"]["action"] == "play/pause":
            self.key_config = key_config
            self.key_config["icon"] = "play.png"
        super().__init__(key_config, stream_deck)

    def action(self) -> None:

        match self.action_data["action"]:
            case "play/pause":
                subprocess.run(
                    [
                        "osascript",
                        "-e",
                        """tell application "Music"
    if (player state as string) is "playing" then
        pause
    else
        play
    end if
end tell""",
                    ]
                )
            case "next":
                subprocess.run(
                    ["osascript", "-e", 'tell application "Music" to next track']
                )
            case "previous":
                subprocess.run(
                    ["osascript", "-e", 'tell application "Music" to previous track']
                )
            case _:
                raise ValueError(f"Invalid action: {self.action_data['action']}")

    def set_image(self):
        if self.action_data["action"] == "play/pause":
            player_state = subprocess.run(
                ["osascript", "-e", 'tell application "Music" to get player state'],
                capture_output=True,
                text=True,
            )

            icon = Image.open(
                config["icon_dir"] + "/" + self.key_config["action_data"]["pause_icon"]
                if player_state.stdout.strip() == "playing"
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
