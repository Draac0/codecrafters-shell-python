from ntpath import isdir
import shelve
import sys
import os
import subprocess
import shlex

def find_executables(cmd: str) -> tuple[str,bool]:
    path = os.environ.get("PATH")
    if not path:
        return ('',False)
    expanded_path = os.path.expandvars(path)
    directories = expanded_path.split(os.pathsep)
    
    for directory in directories:
        if not directory or not os.path.isdir(directory):
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                if os.access(file_path, os.X_OK) and os.path.isfile(file_path) and cmd == file:
                    return (file_path, True)
    
    return ('',False)

def type_cmd(cmd: str):
    cmd_parts = cmd.split(maxsplit=1)
    if (len(cmd_parts) < 2):
        sys.stdout.write(f"Invalid cmd\n")
        return
    type_part = cmd_parts[1]
    valid_cmds = ['type', 'exit', 'echo', 'pwd']
    if type_part in valid_cmds:
        sys.stdout.write(f"{type_part} is a shell builtin\n")
        return
    
    file_path, found = find_executables(type_part)
    if found:
        sys.stdout.write(f"{type_part} is {file_path}\n")
        return    
    sys.stdout.write(f"{type_part}: not found\n")
            
def echo_cmd(cmd: str):
    cmd_parts = cmd.split(maxsplit=1)
    echo_content = cmd_parts[1]
    sys.stdout.write(f"{echo_content}\n")

def exec_cmd(cmd: str):
    cmd_parts = shlex.split(cmd)
    subprocess.run(cmd_parts)

def exec_pwd():
    sys.stdout.write(f"{os.getcwd()}\n")
    
def exec_cd(cmd: str):
    parts = shlex.split(cmd)
    if len(parts) != 2:
        return
    path = parts[1]
    if parts[1] == '~':
        path = os.environ.get('HOME')
    if os.path.isdir(path):
        os.chdir(path)
    else:
        sys.stdout.write(f"cd: {path}: No such file or directory\n")

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == 'exit':
            break
        elif command.startswith("echo"):
            echo_cmd(command)
        elif command.startswith("type"):
            type_cmd(command)
        elif command == "pwd":
            exec_pwd()
        elif "cd" == shlex.split(command)[0]:
            exec_cd(command)
        elif find_executables(shlex.split(command)[0])[1]:
            exec_cmd(command)
        else:
            sys.stdout.write(f"{command}: command not found\n")


if __name__ == "__main__":
    main()
