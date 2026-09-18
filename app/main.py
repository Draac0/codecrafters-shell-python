import sys
import os

def find_executables(cmd: str) -> bool:
    path = os.environ.get("PATH")
    if not path:
        return False
    expanded_path = os.path.expandvars(path)
    directories = expanded_path.split(os.pathsep)
    
    for directory in directories:
        if not directory or not os.path.isdir(directory):
            continue
        
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                if os.access(file_path, os.X_OK) and os.path.isfile(file_path) and cmd == file:
                    sys.stdout.write(f"{cmd} is {file_path}\n")
                    return True
    
    return False

def type_cmd(cmd: str):
    cmd_parts = cmd.split(maxsplit=1)
    if (len(cmd_parts) < 2):
        sys.stdout.write(f"Invalid cmd\n")
        return
    type_part = cmd_parts[1]
    valid_cmds = ['type', 'exit', 'echo']
    if type_part in valid_cmds:
        sys.stdout.write(f"{type_part} is a shell builtin\n")
        return
    
    result = find_executables(type_part)
    if result:
        return    
    sys.stdout.write(f"{type_part}: not found\n")
            

def main():
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
