import subprocess
import re


def red(text):
    return f"\033[31m{text}\033[0m"


def green(text):
    return f"\033[32m{text}\033[0m"


def underline(text):
    return f"\033[4m{text}\033[0m"


def pull_repo():
    try:
        subprocess.run(["git", "pull"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error pulling repository: {e}")
        exit(1)


def get_prev_tag_name():
    try:
        res = subprocess.run(["git", "tag"], check=True, capture_output=True, text=True)
        return res.stdout.splitlines()[-1]
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving tags: {e}")
        exit(1)


def check_tag(tag_name: str):
    pattern = r"^v\d+\.\d+$"
    if not re.match(pattern, tag_name):
        print(f"Tag name '{tag_name}' is not valid. Valid format is vX.Y")
        exit(1)


def main():
    print("")
    print(underline("Clutchwars Resouce Pack Tag Creator"))
    print("")
    print(green("* This script creates a git tag, pushes it to the remote server,"))
    print(green("* which will then trigger a release of the pack on GitHub. "))
    print("")
    print(red("!! Make sure to run this in the resource pack repository !!"))

    prev_tag = get_prev_tag_name()
    print(green(f"Previous tag: {prev_tag}"))
    print(underline("* Please try to increment the version based on this tag"))
    print("\n")

    print("Pulling repository...")
    pull_repo()
    print("Done!")

    tag = input("Enter the tag name to create (press Enter with no value to auto-generate the tag)': ")
    if tag.lower() == "":
        major, minor = map(int, prev_tag[1:].split("."))
        minor += 1
        tag = f"v{major}.{minor}"
    else:
        check_tag(tag)

    try:
        subprocess.run(["git", "tag", "-a", tag, "-m", f"'{tag}'"], check=True)
        print(f"Tag '{tag}' created successfully")

        print("Pushing tag to remote...")
        subprocess.run(["git", "push", "--tags"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error creating tag: {e}")

    print("Done!")
    print(green("Run the following commands to update the resource pack on the server:"))
    print(green("  /clutch reload"))
    print(green("  /clutch resend"))


if __name__ == "__main__":
    main()
