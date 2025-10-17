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


def main():
    update()


if __name__ == "__main__":
    main()
