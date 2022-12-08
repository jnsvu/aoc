import math

f = open("data.txt")
treemap = [l.strip() for l in f.readlines()]
directions = [-1, 0], [1, 0], [0, 1], [0, -1]

def get_tree(y, x):
  return int(treemap[y][x])

def check_visibility(tree, y, x, dir, view_dist):
    if x == 0 or y == 0 or y == len(treemap) - 1 or x == len(treemap[0]) - 1:
        return True, view_dist

    next_y = y + dir[0]
    next_x = x + dir[1]

    if get_tree(next_y, next_x) >= tree:
        return False, view_dist + 1
  
    return check_visibility(tree, next_y, next_x, dir, view_dist + 1)


visibility_count = 0
max_scenic_score = 0

for y in range(len(treemap)):
    for x in range(len(treemap[y])):
      tree = get_tree(y, x)
      grouped_by_direction = [check_visibility(tree, y, x, dir, 0) for dir in directions]
      visibility_for_directions, dist_for_directions = list(zip(*grouped_by_direction))

      visibility_count += 1 if True in visibility_for_directions else 0

      scenic_score = math.prod(dist_for_directions)
      max_scenic_score = scenic_score if scenic_score > max_scenic_score else max_scenic_score

print(visibility_count, max_scenic_score)