f = open("data.txt")

x_register = 1
cycle = 0
signal_strengths = []
# p2
crt_drawing = ""

for l in f.readlines():
    l = l.strip().split(" ")

    if len(l) == 1:
        cycles_added = 1
        v = 0
    else:
        v = int(l[1])
        cycles_added = 2

    for i in range(cycles_added):
        cycle += 1

        if cycle <= 220 and cycle % 40 == 20:
            signal_strengths.append(cycle * x_register)

        # p2
        pos = (cycle - 1) % 40
        
        pixel = "#" if pos in range(x_register - 1, x_register + 2) else "."
        crt_drawing += pixel

        if pos == 39: crt_drawing += "\n"
            
    x_register += v

print(sum(signal_strengths))
print(crt_drawing)
