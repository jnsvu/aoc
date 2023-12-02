f = open("data.txt")
direction_map = {'L': [-1, 0], 'R': [1, 0], 'U': [0, -1], 'D': [0, 1]}
h_pos = (0, 0)
t_pos = (0, 0)
t_pos_log = set()

# p 2
rope_positions = [(0, 0)] * 9
rope_9_log = set()


def get_next_pos(current_pos, direction):
    next_x = current_pos[0] + direction[0]
    next_y = current_pos[1] + direction[1]

    return (next_x, next_y)


def resolve_next_rope_pos(current_pos, predecessor_pos):
    diff_x = predecessor_pos[0] - current_pos[0]
    diff_y = predecessor_pos[1] - current_pos[1]
    next_direction = [0, 0]

    if abs(diff_x) == 2 and abs(diff_y) == 2:
        next_direction[0] = int(diff_x / 2)
        next_direction[1] = int(diff_y / 2)

    elif abs(diff_x) == 2:
        next_direction[0] = int(diff_x / 2)
        next_direction[1] = diff_y

    elif abs(diff_y) == 2:
        next_direction[1] = int(diff_y / 2)
        next_direction[0] = diff_x

    return get_next_pos(current_pos, next_direction)


for l in f.readlines():
    l = l.strip()
    direction, move_count_str = l.split(" ")
    move_count = int(move_count_str)

    for c in range(move_count):
        h_pos = get_next_pos(h_pos, direction_map[direction])
        t_pos = resolve_next_rope_pos(t_pos, h_pos)
        t_pos_log.add(t_pos)

        # p2
        rope_positions[0] = t_pos
        for i in range(1, len(rope_positions)):
            rope_positions[i] = resolve_next_rope_pos(
                rope_positions[i], rope_positions[i - 1])

        rope_9_log.add(rope_positions[8])


print(len(t_pos_log), len(rope_9_log))
