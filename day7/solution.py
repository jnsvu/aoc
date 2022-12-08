f = open("data.txt")
path = []
file_size_by_path = {"/": 0}

def get_path():
    return "_".join(path)

def get_dir_names_from_path():
    return ["_".join(path[:i+1]) for i in range(len(path))]

for cmd in f.readlines():
    cmd = cmd.strip()

    if cmd == "$ cd /":
        path = ["/"]

    elif cmd == "$ cd .." and path:
        path.pop()

    elif cmd.startswith("$ cd "):
        dir = cmd.split(" ")[2]
        path.append(dir)
        if get_path() not in file_size_by_path:
            file_size_by_path[get_path()] = 0

    elif cmd.split(" ")[0].isnumeric():
        for dir in get_dir_names_from_path():
            file_size_by_path[dir] += int(cmd.split(" ")[0])


sum = 0

for a, b in file_size_by_path.items():
    if (b <= 100000):
        sum += b


DISK_SPACE = 70000000
SPACE_REQUIRED = 30000000
AVAILABLE_SPACE = DISK_SPACE - file_size_by_path["/"]
smallest = AVAILABLE_SPACE

for a, b in file_size_by_path.items():
    if AVAILABLE_SPACE + b > SPACE_REQUIRED and b < smallest:
        smallest = b
    
print(smallest)