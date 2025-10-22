class InstallHyprland:
    def __init__(self):
        # Initialize internal logs
        self.log = ''
        self.error = ''
        self.log_file_name = 'full_log.txt'
        self.error_log_file_name = 'error_log.txt'

    def _install_pkg(self, packages_name: list) -> None:
        """Installs a package using pacman"""
        import subprocess
        try:
            result = subprocess.run(
                ["sudo", "pacman", "-S", "--noconfirm"] + packages_name,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
        except Exception as e:
            out = "Exception"
            self.log_message(out, (e).strip())
        else:
            if result.returncode == 0:
                out = "Success"
                self.log_message(out, (result.stdout).strip())
            else:
                out = "Failed"
                self.log_message(out, (result.stderr).strip(), error=True)

    # zsh
    def install_zsh(self) -> None:
        """Installs Zsh shell"""
        print("Zsh: ", end="", flush=True)
        packages = [
            "zsh",
            "zsh-autosuggestions",
            "zsh-syntax-highlighting",
            "zsh-history-substring-search",
            "fzf"
        ]
        self._install_pkg(packages)

    def config_shell_zsh(self) -> None:
        """Sets Zsh as the default shell for the current user"""
        print("Config Shell: ", end="", flush=True)
        import subprocess
        import getpass
        import os
        import shutil
        try:
            # default config
            user = getpass.getuser()
            result = subprocess.run(
                ["sudo", "chsh", "-s", "/bin/zsh", user],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            # ensure zshrc exists
            base_dir = os.path.dirname(os.path.abspath(__file__))
            src_zrc = os.path.join(base_dir, "config", "zsh", ".zshrc")
            zrc = os.path.expanduser("~/.zshrc")
            os.makedirs(os.path.dirname(zrc), exist_ok=True)
            if os.path.exists(src_zrc):
                shutil.copy2(src_zrc, zrc)
            else:
                with open(zrc, "w", encoding="utf-8") as f:
                    f.write("# zsh\n")
        except Exception as e:
            out = "Exception"
            self.log_message(out, (e).strip())
        else:
            if result.returncode == 0:
                out = "Success"
                self.log_message(out, (result.stdout).strip())
            else:
                out = "Failed"
                self.log_message(out, (result.stderr).strip(), error=True)

    def paste_config(self) -> None:
        """Paste the configuration files"""
        print("Config paste: ", end="", flush=True)
        try:
            import os
            from datetime import datetime
            import shutil
            base_dir = os.path.dirname(os.path.abspath(__file__))
            date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            old_config = os.path.join(base_dir, f"old_configs/{date_str}")
            os.makedirs(old_config, exist_ok=True)

            # backup old config
            home_dir = os.path.expanduser("~")
            config_dir = os.path.join(home_dir, ".config")
            if os.path.exists(config_dir):
                shutil.copytree(
                    config_dir, os.path.join(
                        old_config, ".config"), dirs_exist_ok=True)
            else:
                os.makedirs(config_dir, exist_ok=True)

            # paste config
            exclude = ["zsh"]

            source_config = os.path.join(base_dir, "config")
            shutil.copytree(
                source_config,
                config_dir,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(*exclude)
            )
        except Exception as e:
            out = "Exception"
            self.log_message(out, (e).strip())
        else:
            out = "Success"
            self.log_message(out, "Configuration files pasted successfully.")

    def install_terminal(self) -> None:
        """Installs the terminal emulator"""
        print("Terminal: ", end="", flush=True)
        packages = [
            "alacritty",
        ]
        self._install_pkg(packages)

    def _paste_log_to_file(self, content: str, error: bool = False) -> None:
        """Saves the log content to a file"""
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(base_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        full_log_path = os.path.join(log_dir, self.log_file_name)
        error_log_path = os.path.join(log_dir, self.error_log_file_name)

        if error:
            with open(error_log_path, "a", encoding="utf-8") as f:
                f.write(content + "\n")
        else:
            with open(full_log_path, "a", encoding="utf-8") as f:
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
            out = "Exception"
            self.log_message(out, (e).strip())
        else:
            if result.returncode == 0:
                out = "Success"
                self.log_message(out, (result.stdout).strip())
            else:
                out = "Failed"
                self.log_message(out, (result.stderr).strip(), error=True)

    def no_sudo_password(self):
        """Configures sudo to not require a password for the current user"""
        print("No passwd: ", end="", flush=True)
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
            result = subprocess.run(
                [
                    "sudo", "bash", "-c",
                    cmd
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
        except Exception as e:
            out = "Exception"
            self.log_message(out, (e).strip())
        else:
            if result.returncode == 0:
                out = "Success"
                self.log_message(out, (result.stdout).strip())
            else:
                out = "Failed"
                self.log_message(out, (result.stderr).strip(), error=True)

    def install_hyprland(self):
        """Installs Hyprland using pacman"""
        print("Hyperland: ", end="", flush=True)
        packages = [
            "hyprland",
        ]
        self._install_pkg(packages)

    def install_fonts(self):
        """Installs necessary fonts using pacman"""
        print("Fonts: ", end="", flush=True)
        fonts = [
            "noto-fonts",
            "noto-fonts-emoji",
            "ttf-dejavu",
            "ttf-liberation",
            "ttf-nerd-fonts-symbols",
            "ttf-nerd-fonts-symbols-mono",
            "ttf-font-awesome",
            # -----------------------
            # old pkg (migrate bspwm)
            # -----------------------
            "ttf-inconsolata",
            "ttf-jetbrains-mono",
            "ttf-jetbrains-mono-nerd",
            "ttf-terminus-nerd",
            "ttf-ubuntu-mono-nerd"
        ]
        self._install_pkg(fonts)

    def main(self):
        """Main function to run the installer"""
        self.update()
        self.no_sudo_password()
        self.install_hyprland()
        self.install_fonts()
        self.install_terminal()

        self.install_zsh()
        self.config_shell_zsh()

        self.paste_config()


if __name__ == "__main__":
    installer = InstallHyprland()
    installer.main()
