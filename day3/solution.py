

import string

f = open("data.txt")

letters = string.ascii_lowercase + string.ascii_uppercase
score = 0

for line in f.readlines():
    line = line.strip()
    firstpart, secondpart = line[:len(line)//2], line[len(line)//2:]
    checked_letters = []

    for l in firstpart:
        
        if l not in checked_letters and l in secondpart:
            score += letters.find(l) + 1

        checked_letters.append(l)
print(score)
