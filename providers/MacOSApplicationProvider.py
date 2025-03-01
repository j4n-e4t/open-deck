import subprocess


class MacOSApplicationProvider:
    def __init__(self):
        pass

    def launch(self, app_name):
        subprocess.run(
            [
                "osascript",
                "-e",
                f'tell application "{app_name}" to activate',
            ]
        )
