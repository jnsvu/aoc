f = open("data.txt")
signal = f.readline().strip()
window = list(signal[:14])
marker = 14

for c in signal[14:]:
    if len(window) != len(set(window)):
        marker += 1
        window.append(c)
        window.pop(0)
        continue
    break

print(marker)
