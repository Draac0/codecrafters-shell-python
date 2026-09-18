import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == 'exit':
            break
        if command.startswith("echo"):
            cmd_parts = command.split(maxsplit=1)
            echo_content = cmd_parts[1]
            sys.stdout.write(f"{echo_content}\n")
        else:
            sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
