def update():
    import subprocess
    result = subprocess.run(
        ["sudo", "pacman", "-Syu"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    if result.returncode == 0:
        print("Update: Success")
    elif result.returncode != 0:
        print("Update: Failed")
    else:
        pass


def no_sudo_password():
    import subprocess
    import getpass
    try:
        user = getpass.getuser()
        sudoers_line = f"{user} ALL=(ALL) NOPASSWD:ALL\n"
        subprocess.run(
            [
                "sudo", "bash", "-c",
                f"echo '{sudoers_line.strip()}' > /etc/sudoers.d/010_no_password && chmod 440 /etc/sudoers.d/010_no_password"
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


def main():
    update()
    no_sudo_password()
    install_hyprland()
    install_fonts()


if __name__ == "__main__":
    main()
