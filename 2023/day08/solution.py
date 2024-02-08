import math

f = open("data.txt")
instructions, lines = f.read().split("\n\n")

lines = lines.split("\n")

d = {}

for line in lines:
    parts = line.split(" = ")
    key = parts[0]
    left = parts[1].split(", ")[0].replace("(", "")
    right = parts[1].split(", ")[1].replace(")", "")

    d[key] = {"L": left, "R": right}


def p1():
    current = "AAA"
    steps = 1
    while True:
        for instruction in instructions:
            next = d[current][instruction]
            if next == "ZZZ":
                print(steps)
                return

            current = next
            steps += 1


def p2():
    start_nodes = [key for key in d.keys() if key.endswith("A")]
    cycles = {node_key: 0 for node_key in start_nodes}

    for node in start_nodes:
        i = 0
        steps = 1
        next_node = node

        while True:
            if i >= len(instructions):
                i = 0

            instruction = instructions[i]
            next_node = d[next_node][instruction]

            if next_node.endswith("Z"):
                cycles[node] = steps
                break

            steps += 1
            i += 1

    print(math.lcm(*cycles.values()))


p1()
p2()
