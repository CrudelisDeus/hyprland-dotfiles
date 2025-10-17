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
        print(f"NO PASSWORD: ERROR {e}")
    else:
        print("NO PASSWORD: OK")


def main():
    update()


if __name__ == "__main__":
    main()
