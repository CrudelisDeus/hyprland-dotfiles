class InstallHyprland:
    def __init__(self):
        # Initialize internal logs
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
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
        except Exception as e:
            out = "Update: Exception"
            print(f"{out}")
            self.log_message(out, str(e), error=True)
        else:
            if result.returncode == 0:
                out = "Update: Success"
                print(out)
                self.log_message(out, (result.stdout).strip())
            else:
                out = "Update: Failed"
                print(out)
                self.log_message(out, (result.stderr).strip(), error=True)


if __name__ == "__main__":
    installer = InstallHyprland()
    installer.update()
