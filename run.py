class InstallHyprland:
    def __init__(self):
        # Initialize internal logs
        self.log = ''
        self.error = ''
        self.log_file_name = 'full_log.txt'
        self.error_log_file_name = 'error_log.txt'

    def _paste_log_to_file(self, content: str, error: bool = False) -> None:
        """Saves the log content to a file"""
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "log")
        os.makedirs(log_dir, exist_ok=True)
        full_log_path = os.path.join(log_dir, self.log_file_name)
        error_log_path = os.path.join(log_dir, self.error_log_file_name)

        with open(full_log_path, "a", encoding="utf-8") as f:
            f.write(content + "\n")

        if error:
            with open(error_log_path, "a", encoding="utf-8") as f:
                f.write(content + "\n")

    def log_message(
            self, message: str, result: str, error: bool = False
            ) -> None:
        """Logs a message to the internal log.
        If error is True, also logs to error log."""
        entry = f"{message}\n{(result or '')}\n"
        self.log += entry
        self._paste_log_to_file(entry)
        if error:
            self.error += entry
            self._paste_log_to_file(entry, error=True)

        print(message)

    def update(self):
        """Updates the system using pacman"""
        print("Update: ", end="", flush=True)
        try:
            import subprocess
            result = subprocess.run(
                ["sudo", "pacman", "-Syu", "--noconfirm"],
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
                out = "Success"
                self.log_message(out, (result.stdout).strip())
            else:
                out = "Failed"
                self.log_message(out, (result.stderr).strip(), error=True)


if __name__ == "__main__":
    installer = InstallHyprland()
    installer.update()
    installer.update()
