import copy
f = open("data.txt")
input = f.read().strip()

shapes = [
    [
        [1, 1, 1, 1]
    ],
    [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ],
    [
        [1, 1, 1],
        [0, 0, 1],
        [0, 0, 1]
    ],
    [
        [1],
        [1],
        [1],
        [1]
    ],
    [
        [1, 1],
        [1, 1],
    ]
]


def add_shape_to_m(pos, shape, m):
    for y in range(pos[1], pos[1] + len(shape)):
        for x in range(pos[0], pos[0] + len(shape[0])):
            shape_value = shape[y - pos[1]][x - pos[0]]
            if shape_value == 1:
                m[y][x] = shape_value

    return m


def print_m(m, shape_pos=None, shape=None):
    m_cpy = copy.deepcopy(m)
    if shape_pos and shape:
        add_shape_to_m(shape_pos, shape, m_cpy)

    m_r = list(reversed(m_cpy))

    for y in range(len(m_r)):
        for x in range(len(m_r[y])):
            l = "." if m_r[y][x] == 0 else "#"
            print(l, end="")
        print("    # " + str(len(m) - y))


def move_down(pos, shape, m):
    # check is bottom
    if pos[1] == 0:
        return pos, True

    next_y = pos[1] - 1

    # check collisions with other shapes
    for y in range(next_y, next_y + len(shape)):
        for x in range(pos[0], pos[0] + len(shape[0])):
            m_value = m[y][x]
            shape_value = shape[y - next_y][x - pos[0]]
            if m_value == 1 and shape_value == 1:
                return pos, True

    return (pos[0], next_y), False


def move_horizontally(dir_str, pos, shape, m):
    dir_x = 1 if dir_str == ">" else -1
    shape_x = 0 if dir_x == -1 else len(shape[0]) - 1
    next_x = pos[0] + dir_x

    # boundaries
    if next_x < 0 or next_x + len(shape[0]) - 1 > len(m[0]) - 1:
        return pos

    # check other shapes at shape heights
    for y in range(pos[1], pos[1] + len(shape)):
        for x in range(next_x, next_x + len(shape[0])):
            m_value = m[y][x]  # [next_x + shape_x]
            shape_value = shape[y - pos[1]][x - next_x]
            if m_value == 1 and shape_value == 1:
                return pos

    return (next_x, pos[1])


input_len = len(input)


def get_height(target_shape_count):
    current_shape_idx = 0
    shape_pos = (2, 3)
    m = [[0 for x in range(7)] for y in range(4)]
    shape_count = 0
    input_idx = 0
    max_y = 0
    cache = {}

    while True:
        shape = shapes[current_shape_idx]
        space_y = len(m) - max_y
        rows_to_add = [[0 for x in range(7)]
                       for y in range(3 + len(shape) - space_y)]
        m.extend(rows_to_add)
        shape_pos = (2, max_y + 3)
        directions = []
        while True:
            dir = input[input_idx]
            shape_pos = move_horizontally(dir, shape_pos, shape, m)
            pos, is_bottom = move_down(shape_pos, shape, m)
            shape_pos = pos
            input_idx = (input_idx + 1) % input_len

            directions.append(dir)

            if is_bottom:
                diff_max_y = max(shape_pos[1] + len(shape), max_y) - max_y
                max_y = max(shape_pos[1] + len(shape), max_y)
                add_shape_to_m(shape_pos, shape, m)

                key = (diff_max_y, current_shape_idx, input_idx,
                       shape_pos[0], len(m) - shape_pos[1])
                cache_value = cache.get(key, (0, []))
                shape_counts = cache_value[1] + [shape_count]
                cache[key] = (cache_value[0] + 1, shape_counts)

                shape_count += 1
                current_shape_idx = (current_shape_idx + 1) % len(shapes)

                if shape_count == target_shape_count:
                    return max_y, cache

                break


# p1
print(get_height(2022)[0])

# p2
_, cache = get_height(100_000)

for duplicate_count, shape_counts in cache.values():
    if duplicate_count > 1:
        cycle = shape_counts[-1:][0] - shape_counts[-2:-1][0]

t = 1_000_000_000_000
cycle_max_y, _ = get_height(cycle)
count_before_cycle = t % cycle
t -= count_before_cycle
max_y_before_cycle, _ = get_height(count_before_cycle)

print(max_y_before_cycle + (t / cycle) * cycle_max_y)
