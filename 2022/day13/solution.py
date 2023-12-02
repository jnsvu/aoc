import json

f = open("data.txt")
input = [[json.loads(arr_str) for arr_str in l.split("\n")] for l in f.read().split("\n\n")]

def flatten(l):
    if l == []:
        return l
    if isinstance(l[0], list):
        return flatten(l[0]) + flatten(l[1:])
    return l[:1] + flatten(l[1:])

def compare(left, right):
    if type(left) is int and type(right) is int:
        if left == right: return None
        return left <= right

    if type(left) is list and type(right) is list:
      for i in range(min(len(left), len(right))):
          l = left[i]
          r = right[i]

          is_right_order = compare(l, r)
          
          if is_right_order is not None:
            return is_right_order

      if len(left) != len(right):
        return len(left) < len(right)

      return None

    if type(left) is list:
      return compare(left, [right])
  
    return compare([left], right)



indices = []
flat_inputs = []
flat_inputs.extend([[[2]], [[6]] ])

for i, [left, right]in enumerate(input):
    # p1
    valid_order = compare(left, right)
    if valid_order: indices.append(i + 1)
  
    # p2
    flat_inputs.append(left)
    flat_inputs.append(right)


print(sum(indices))

# p2
idx_1 = sum([1 for e in flat_inputs  if compare(e, [[2]])]) + 1
idx_2 = sum([1 for e in flat_inputs  if compare(e, [[6]])])  + 1

print(idx_1 * idx_2)