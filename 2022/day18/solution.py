import math

f = open("data.txt")


input = [tuple([int(n) for n in l.strip().split(",")]) for l in f.readlines()]
max_x, max_y, max_z = [-math.inf] * 3
min_x, min_y, min_z = [math.inf] * 3


for i in range(len(input)):
    x, y, z = input[i]
    max_x = max(max_x, x)
    max_y = max(max_y, y)
    max_z = max(max_z, z)

    min_x = min(min_x, x)
    min_y = min(min_y, y)
    min_z = min(min_z, z)


def get_nbs(pos):
    x, y, z = pos
    adj_x = [(x - 1, y, z), (x + 1, y, z)]
    adj_y = [(x, y - 1, z), (x, y + 1, z)]
    adj_z = [(x, y, z - 1), (x, y, z + 1)]

    return adj_x + adj_y + adj_z


def out_of_bounds(pos):
    return not (
        min_x <= pos[0] <= max_x
        and min_y <= pos[1] <= max_y
        and min_z <= pos[2] <= max_z
    )


def not_trapped_air(pos):
    visited = {pos}
    q = [pos]

    while q:
        current = q.pop(0)
        for adj in get_nbs(current):
            if adj not in visited:
                if out_of_bounds(adj):
                    return True, {p: True for p in visited}
                if adj not in input:
                    visited.add(adj)
                    q.append(adj)

    return False, {p: False for p in visited}


surface = 0
exterior_surface = 0
cache = {}

for i in range(len(input)):
    x, y, z = input[i]
    adj_cubes = [a for a in get_nbs(input[i]) if a in input]
    surface += 6

    for a in get_nbs(input[i]):
        # not visible surface
        if a in input:
            surface -= 1

          # is air cube
        else:
            if a in cache:
                is_not_trapped = cache[a]
            else:
                is_not_trapped, visited = not_trapped_air(a)
                cache = cache | visited
            exterior_surface += 1 if is_not_trapped else 0


# p1
print(surface)

# p2
print(exterior_surface)
