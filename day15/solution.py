f = open("data.txt")

data = [l.split(":") for l in f.readlines()]
sensors = []  # [((8, 7), (2, 10))]
beacons = []  # [(2, 10)]

space = 4_000_000


for l in data:
    sensor_pos = eval(l[0].split("x=")[1].replace("y=", ""))
    closest_beacon_pos = eval(l[1].split("x=")[1].replace("y=", ""))
    sensors.append((sensor_pos, closest_beacon_pos))
    beacons.append(closest_beacon_pos)


def check_row(y_to_check):
    no_beacon_locations = set()
    for sensor_pos, closest_beacon_pos in sensors:
        diff_x = closest_beacon_pos[0] - sensor_pos[0]
        diff_y = closest_beacon_pos[1] - sensor_pos[1]
        manhattan_dist = abs(diff_x) + abs(diff_y)

        dist_from_y_to_check = abs(sensor_pos[1] - y_to_check)

        if dist_from_y_to_check > manhattan_dist:
            continue

        y = manhattan_dist - dist_from_y_to_check
        start = sensor_pos[0] - y
        end = sensor_pos[0] + y + 1

        for x in range(start, end):
            pos = (x, y_to_check)
            if pos in beacons:
                continue

            no_beacon_locations.add(pos)

    return no_beacon_locations


# p1
no_beacon_spots = check_row(2_000_000)
print(len(no_beacon_spots))


def union(row):
    l = []
    for begin, end in sorted(row):
        if l and l[-1][1] > begin - 1:
            l[-1][1] = max(l[-1][1], end)
        else:
            l.append([begin, end])
    return l


def check_row_p2(y_to_check):
    intervals = []

    for sensor_pos, closest_beacon_pos in sensors:
        diff_x = closest_beacon_pos[0] - sensor_pos[0]
        diff_y = closest_beacon_pos[1] - sensor_pos[1]
        manhattan_dist = abs(diff_x) + abs(diff_y)

        dist_from_y_to_check = abs(sensor_pos[1] - y_to_check)

        if dist_from_y_to_check > manhattan_dist:
            continue

        y = manhattan_dist - dist_from_y_to_check
        start = min(max(sensor_pos[0] - y, 0), space)
        end = max(min(sensor_pos[0] + y + 1, space), 0)

        intervals.append((start, end))

    return intervals


for y in range(space + 1):
    row = check_row_p2(y)
    row = union(row)

    if len(row) > 1:
        print(row[0][1] * space + y)
