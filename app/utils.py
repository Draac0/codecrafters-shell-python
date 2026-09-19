from typing import Optional
import os



def find_unquoted_redirect(cmd: str) -> Optional[tuple[str, int, bool]]:
    i = 0
    in_single = in_double = False
    n = len(cmd)
    
    def check_if_append(i: int) -> bool:
        return True if cmd[i+1] == '>' else False
    while i<n:
        if cmd[i] == "'" and not in_double:
            in_single = not in_single
        elif cmd[i] == '"' and not in_single:
            in_double = not in_double
        elif cmd[i] == '>' and not in_single and not in_double:
            if i>0 and cmd[i-1] == '1':
                return ('1>', i-1, check_if_append(i))
            elif i>0 and cmd[i-1] == '2':
                return ('2>', i-1, check_if_append(i))
            return ('>', i, check_if_append(i))
        i+=1
    return None


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

def list_all_path_executables() -> list[str]:
    path = os.environ.get("PATH")
    if not path:
        return []
    
    result = []
    expanded_path = os.path.expandvars(path)
    directories = expanded_path.split(os.pathsep)
    
    for directory in directories:
        if not directory or not os.path.isdir(directory):
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                if os.access(file_path, os.X_OK) and os.path.isfile(file_path):
                    result.append(file)
    print(result)
    return result