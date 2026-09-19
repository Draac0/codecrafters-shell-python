from ntpath import isdir
import shelve
import sys
import os
import subprocess
import shlex
from app.utils import find_executables, find_unquoted_redirect


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
    cmd_parts = shlex.split(cmd)
    echo_content = " ".join(cmd_parts[1:])
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
        
def exec_redirect(cmd: str) -> None:
    result = find_unquoted_redirect(cmd)
    if not result:
        return
    sign, index, is_append = result
    
    cmd_part = cmd[:index]
    cmd_split = shlex.split(cmd_part)
    cmd_exec_result = subprocess.run(cmd_split, capture_output=True, text=True)
    
    write_to_file = cmd_exec_result.stdout
    if sign == '2>':
        sys.stdout.write(f"{cmd_exec_result.stdout}")
        write_to_file = cmd_exec_result.stderr
    elif cmd_exec_result.returncode != 0:
        sys.stdout.write(f"{cmd_exec_result.stderr}")
    add_one = 1 if is_append else 0
    if sign == '>':
        file_path = cmd[index+1+add_one:].strip()
    else:
        file_path = cmd[index+2+add_one:].strip()
    file_mode = 'a' if is_append else 'w'
    with open(file_path, file_mode) as file:
        file.write(write_to_file)
    

def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == 'exit':
            break
        elif find_unquoted_redirect(command):
            exec_redirect(command)
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
