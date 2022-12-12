from queue import Queue
import string

input = open("data.txt").readlines()


for y in range(len(input)):
    input[y] = input[y].strip()
    for x, c in enumerate(input[y]):
        if c == "S":
            start = (y, x)
            input[y] = input[y].replace("S", "a")

        if c == "E":
            end = (y, x)
            input[y] = input[y].replace("E", "z")


def get_char(pos):
    return input[pos[0]][pos[1]]


def is_valid_nb(pos, nb_pos):
    if nb_pos[0] < 0 or nb_pos[1] < 0 or nb_pos[0] > len(input) - 1 or nb_pos[1] > len(input[0]) - 1:
        return False

    diff = string.ascii_lowercase.find(
        get_char(nb_pos)) - string.ascii_lowercase.find(get_char(pos))

    return diff <= 1


def get_neighbours(pos):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbour_positions = [(pos[0] + dir[0], pos[1] + dir[1])
                           for dir in directions]
    valid_neighours = [
        nb_pos for nb_pos in neighbour_positions if is_valid_nb(pos, nb_pos)]

    return valid_neighours


def bfs(start_pos, end_pos):
    g = {}
    q = Queue()
    q.put(start_pos)
    checked = set()
    checked.add(start_pos)
    while not q.empty():
        loc = q.get()

        if loc == end_pos:
            return g

        for nb_pos in get_neighbours(loc):
            if nb_pos not in checked:
                checked.add(nb_pos)
                q.put(nb_pos)
                g[str(nb_pos)] = loc

    return g


def graph_to_path(g):
    path = []
    current_pos = end
    while current_pos:
        if not str(current_pos) in g:
            break
        current_pos = g[str(current_pos)]
        path.append(current_pos)

    return path


# p1
graph = bfs(start, end)
print(len(graph_to_path(graph)))

# p2
start_positions = [[(y, i) for i in range(len(row)) if row[i] == "a"]
                   for y, row in enumerate(input) if "a" in row]

start_positions = [item for sublist in start_positions for item in sublist]

res = [len(graph_to_path(bfs(sp, end))) for sp in start_positions]
res = [r for r in res if r != 0]
print(min(res))
