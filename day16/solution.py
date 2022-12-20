f = open("data.txt")

valves = {}

for l in f.readlines():
    l = l.strip()
    valve = l.split(" has")[0][-2:]

    rate = int(l.split("rate=")[1].split(";")[0])
    leads_to = l.split("valve")[1].replace(
        "s ", "").replace(" ", "").split(",")

    valves[valve] = {
        "rate": rate,
        "leads_to": leads_to
    }

feasible_valves = [v for v, data in valves.items() if data["rate"] > 0]


def get_flow_rate(open_valves):
    return sum([valves[v]["rate"] for v in open_valves])


def all_feasible_opened(open_velves):
    return len(feasible_valves) == len(open_velves)


def get_cache_key_p1(v, open_valves, minutes):
    return (v, tuple(open_valves), minutes)


def dfs_p1(v, minutes, pressure, open_valves, pressure_map):
    v_data = valves[v]

    key = get_cache_key_p1(v, open_valves, minutes)
    if pressure_map.get(key, -1) >= pressure:
        return pressure

    pressure_map[get_cache_key_p1(v, open_valves, minutes)] = pressure

    if minutes <= 0:
        return pressure

    flow_rate_all = get_flow_rate(open_valves)
    next_pressure = pressure + flow_rate_all
    v_flow_rate = v_data["rate"]

    # if opens valve
    opened_pressure = 0
    if v_flow_rate != 0 and v not in open_valves:
        open_valves_cpy = open_valves.union([v])
        opened_pressure = dfs_p1(
            v, minutes - 1, next_pressure, open_valves_cpy, pressure_map)

    # move to next room
    next_pressures = [dfs_p1(next_v, minutes - 1, next_pressure, open_valves, pressure_map)
                      for next_v in v_data["leads_to"]]

    max_pressure = max(opened_pressure, *next_pressures)

    return max_pressure


def get_cache_key_p2(minutes, v, ev):
    return (minutes, v, ev)


max_pressure_p2 = 0


def dfs_p2(v, ev, minutes, pressure, open_valves, pressure_map):
    global max_pressure_p2
    v_data = valves[v]
    ev_data = valves[ev]
    pressure += get_flow_rate(open_valves)

    if pressure_map.get(get_cache_key_p2(minutes, v, ev), -1) >= pressure:
        return

    pressure_map[get_cache_key_p2(minutes, v, ev)] = pressure

    if minutes <= 1:
        max_pressure_p2 = max(pressure, max_pressure_p2)
        return

    # wait for time to end
    if all_feasible_opened(open_valves):
        return dfs_p2(v, ev, minutes - 1, pressure, open_valves, pressure_map)

    v_flow_rate = v_data["rate"]
    ev_flow_rate = ev_data["rate"]

    # v opens
    if v_flow_rate != 0 and v not in open_valves:
        # both open
        if ev_flow_rate != 0 and ev not in open_valves:
            dfs_p2(
                v, ev, minutes - 1, pressure, open_valves.union([v, ev]), pressure_map)

        # v opens and move ev to next room
        [dfs_p2(v, next_ev, minutes - 1, pressure, open_valves.union([v]), pressure_map)
         for next_ev in ev_data["leads_to"]]

    # move v
    for next_v in v_data["leads_to"]:
        # ev opens
        if ev_flow_rate != 0 and ev not in open_valves:
            dfs_p2(
                next_v, ev, minutes - 1, pressure, open_valves.union([ev]), pressure_map)

        # move v and ev
        [dfs_p2(next_v, next_ev, minutes - 1, pressure, open_valves, pressure_map)
         for next_ev in ev_data["leads_to"]]


# p1
print(dfs_p1("AA", 30, 0, set(),  {}))

# p2
dfs_p2("AA", "AA", 26, 0, set(),  {})
print(max_pressure_p2)
