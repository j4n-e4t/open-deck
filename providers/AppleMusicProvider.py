import subprocess


class AppleMusicProvider:
    def __init__(self):
        pass

    def play_pause(self):
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

    def next(self):
        subprocess.run(["osascript", "-e", 'tell application "Music" to next track'])

    def previous(self):
        subprocess.run(
            ["osascript", "-e", 'tell application "Music" to previous track']
        )

    def is_playing(self):
        player_state = subprocess.run(
            [
                "osascript",
                "-e",
                """
                    if application "Music" is running then
                        tell application "Music" to get player state
                    else
                        return "stopped"
                    end if
                """,
            ],
            capture_output=True,
            text=True,
        )
        return player_state.stdout.strip() == "playing"
