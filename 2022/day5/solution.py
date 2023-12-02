

f = open("data.txt")
stacks = []
stack_initialized = False

for line in f.readlines():
    if line.strip().startswith("["):
        n = 4
        line = [line[i:i+n] for i in range(0, len(line), n)]
        line = [x.strip() for x in line]
        stacks.append(line)
        continue
    elif not stack_initialized:
        stack_initialized = True
        stacks = [[x for x in reversed(list(a)) if x != ""]
                  for a in zip(*(stacks))]

    if line.strip().startswith("m"):
        line = line.strip().split(" ")
        n_stacks = int(line[1])
        _from = int(line[3]) - 1
        _to = int(line[5]) - 1

        moved_stacks = stacks[_from][-n_stacks:]
        stacks[_from] = stacks[_from][:-n_stacks]
        stacks[_to].extend(reversed(moved_stacks))

print([x[-1:] for x in stacks])
