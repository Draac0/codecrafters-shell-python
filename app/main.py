import sys

def type_cmd(cmd: str):
    cmd_parts = cmd.split(maxsplit=1)
    if (len(cmd_parts) < 2):
        sys.stdout.write(f"Invalid cmd\n")
        return
    type_part = cmd_parts[1]
    valid_cmds = ['type', 'exit', 'echo']
    if type_part in valid_cmds:
        sys.stdout.write(f"{type_part} is a shell builtin\n")
    else:
        sys.stdout.write(f"{type_part}: not found\n")
            

def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == 'exit':
            break
        elif command.startswith("echo"):
            cmd_parts = command.split(maxsplit=1)
            echo_content = cmd_parts[1]
            sys.stdout.write(f"{echo_content}\n")
        elif command.startswith("type"):
            type_cmd(command)
        else:
            sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
