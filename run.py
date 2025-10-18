class InstallHyprland:
    def __init__(self):
        self.log = ''
        self.error = ''

    def log_message(
            self, message: str, result: str, error: bool = False
            ) -> None:
        """Logs a message to the internal log.
        If error is True, also logs to error log."""
        self.log += message + '\n'
        self.log += result + '\n'
        if error:
            self.error += message + '\n'
            self.error += result + '\n'

        print(self.log)
        print("-----")
        print(self.error)

    def update(self):
        try:
            import subprocess
            result = subprocess.run(
                ["sudo", "pacman", "-Syu"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
            )
        except Exception:
            out = "Update: Failed"
            print(f"{out}")
            self.log_message(out, result.stderr.strip(), error=True)
        else:
            out = "Update: Success"
            print(out)
            self.log_message(out, result.stdout.strip())

    def no_sudo_password():
        import subprocess
        import getpass
        try:
            user = getpass.getuser()
            sudoers_line = f"{user} ALL=(ALL) NOPASSWD:ALL\n"
            cmd = (
                f"echo '{sudoers_line.strip()}' "
                "> /etc/sudoers.d/010_no_password && "
                "chmod 440 /etc/sudoers.d/010_no_password"
            )
            subprocess.run(
                [
                    "sudo", "bash", "-c",
                    cmd
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"No password: Failed {e}")
        else:
            print("No password: Success")

    def install_hyprland():
        import subprocess
        try:
            subprocess.run(
                ["sudo", "pacman", "-S", "--noconfirm", "hyprland"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"Install Hyprland: Failed {e}")
        else:
            print("Install Hyprland: Success")

    def install_fonts():
        import subprocess
        fonts = [
            "noto-fonts",
            "noto-fonts-emoji",
            "ttf-dejavu",
            "ttf-liberation",
            "ttf-nerd-fonts-symbols",
            "ttf-nerd-fonts-symbols-mono",
            "ttf-font-awesome"
        ]
        try:
            subprocess.run(
                ["sudo", "pacman", "-S", "--noconfirm"] + fonts,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            print(f"Install Fonts: Failed {e}")
        else:
            print("Install Fonts: Success")

    def main(self):
        self.update()
        self.no_sudo_password()
        self.install_hyprland()
        self.install_fonts()


if __name__ == "__main__":
    InstallHyprland().main()
