
scoreMappings = {
  'X': 1,
  'Y': 2,
  'Z': 3,
  'W': 6,
  'D': 3,
  'L': 0
}

winLoseMap = {
  'A': {
    'X':'D',
    'Y': 'W' ,
    'Z': 'L'
  },
  'B': {
    'X':'L',
    'Y': 'D' ,
    'Z': 'W'
  },
  'C': {
    'X':'W',
    'Y': 'L' ,
    'Z': 'D'
  },
}

score = 0

with open('data.txt') as f:
  for line in f.readlines():
    my = line[2]
    opp = line[0]

    score += scoreMappings[my]
    score += scoreMappings[winLoseMap[opp][my]]


print(score)
