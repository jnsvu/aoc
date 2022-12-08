

f = open("data.txt")

res = 0

for line in f.readlines():
    line = line.strip()
    line = [x.split("-") for x in line.split(",")]

    first = [int(line[0][0]), int(line[0][1])]
    second = [int(line[1][0]), int(line[1][1])]

    if first[0] >= second[0] and first[1] <= second[1]:
        res += 1
        continue

    if second[0] >= first[0] and second[1] <= first[1]:
        res += 1

print(res)
