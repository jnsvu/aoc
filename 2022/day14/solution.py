from termcolor import colored
f = open("data.txt")

input = [l.strip().split(" -> ") for l in f.read().split("\n")]
input = [[(int(i.split(",")[0]), int(i.split(",")[1]))
          for i in l] for l in input]


def get_rocks():
    rocks = []
    for y in range(len(input)):
        for x in range(1, len(input[y])):
            pos = input[y][x]
            prev_pos = input[y][x - 1]
            min_x = min(prev_pos[0], pos[0])
            max_x = max(prev_pos[0], pos[0])
            min_y = min(prev_pos[1], pos[1])
            max_y = max(prev_pos[1], pos[1])
            line_pos_x = [x for x in range(min_x, max_x + 1)]
            line_pos_y = [y for y in range(min_y, max_y + 1)]
            # make lists the same length
            line_pos_y = line_pos_y if len(
                line_pos_y) > 1 else line_pos_y * len(line_pos_x)
            line_pos_x = line_pos_x if len(
                line_pos_x) > 1 else line_pos_x * len(line_pos_y)
            line_pos = list(zip(line_pos_x, line_pos_y))
            rocks.extend(line_pos)

    return rocks


def print_map(rocks, sand):
    x_pos = [r[0] for r in sand]
    min_x = min(x_pos)
    max_x = 650 # max(x_pos)

    y_pos = [r[1] for r in sand]
    min_y = min(y_pos)
    max_y = max(y_pos)
    print(min_x, max_x)

    for y in range(min_y, max_y + 1):
        print()
        for x in range(min_x, max_x + 1):
            if (x, y) in sand:
                idx = sand.index((x, y)) 
                is_last = idx == len(sand) - 1
                if is_last:
                    print(colored('o', 'red'), end="")
                else:
                    print(colored("o", 'yellow'), end="")

            elif (x, y) in rocks:
                print(colored('#', 'white'), end="")

            else:
                print(colored(".", "grey"), end="")


def is_abyss(curr_pos, rock_list):
    x_pos = curr_pos[0]
    rocks_south = [pos[0] for pos in rock_list if pos[1]
                   >= curr_pos[1] and x_pos == pos[0]]

    return len(rocks_south) == 0


def is_rock_or_sand(pos, sand_list, rock_list, max_y):
    return pos in sand_list or pos in rock_list or (max_y != None and pos[1] == max_y)


def get_new_sand_pos(curr_pos, sand_list, rock_list, max_y):

    # try south
    south_pos = (curr_pos[0], curr_pos[1] + 1)
    if not is_rock_or_sand(south_pos, sand_list, rock_list, max_y):
        # print("SOUTH")
        return south_pos

    # try south-west
    # west_pos = (curr_pos[0] - 1, curr_pos[1])
    south_west_pos = (curr_pos[0] - 1, curr_pos[1] + 1)
    # print("SOUTH_WESTT")
    if not True in [is_rock_or_sand(_pos, sand_list, rock_list, max_y) for _pos in [ south_west_pos]]:
        return south_west_pos

    # try south_east
    # east_pos = (curr_pos[0] + 1, curr_pos[1])
    south_east_pos = (curr_pos[0] + 1, curr_pos[1] + 1)
    if not True in [is_rock_or_sand(pos, sand_list, rock_list, max_y) for pos in [ south_east_pos]]:
        # print("SOUTH_EAST")
        return south_east_pos

    return curr_pos
  

rocks = get_rocks()
sand = []
current_sand_idx = 0

def move_sand(idx, sand_list, rock_list, max_y=None):
    prev_pos = None
    while sand_list[idx] != prev_pos:
      tmp = sand_list[idx]
      new_sand_pos = get_new_sand_pos(tmp, sand_list, rock_list, max_y)
      sand_list[idx] = new_sand_pos
      prev_pos = tmp

      if  max_y == None and is_abyss(sand_list[idx], rock_list):
          return True

    return False

while True:
    sand.append((500, 0))
    if move_sand(current_sand_idx, sand, rocks): break
    current_sand_idx += 1

# p1
print_map(rocks, sand)
print(current_sand_idx )

# p2
print("Run p2")
highest_y = max([pos[1] for pos in rocks ]) + 2

while True:
  sand.append((500, 0))
  curr = sand[current_sand_idx]
  if curr == get_new_sand_pos(curr, sand,  rocks, highest_y): break
  move_sand(current_sand_idx, sand, rocks, highest_y)

  current_sand_idx += 1 

print_map(rocks, sand)
print(current_sand_idx + 1)
  
