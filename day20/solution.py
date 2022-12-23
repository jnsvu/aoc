f = open("data.txt")
lines = f.readlines()


def get_encrypted_input():
    return [int(num) for num in lines]


def get_decoded_input(input):

    next_idx_to_move = 0
    idx = 0

    while next_idx_to_move != len(input):
        current_idx = idx % len(input)
        num, move_idx = input[current_idx]

        if move_idx != next_idx_to_move:
            idx += 1
            continue

        if num == 0:
            next_idx_to_move += 1
            continue

        next_idx = (current_idx + num) % (len(input) - 1)
        input.insert(next_idx, input.pop(current_idx))

        next_idx_to_move += 1

    return input


def get_sum(decoded_input):
    encrypted_zero_idx = get_encrypted_input().index(0)
    decoded_zero_pos = decoded_input.index((0, encrypted_zero_idx))
    return sum([decoded_input[(decoded_zero_pos + n) % len(decoded_input)][0] for n in [1000, 2000, 3000]])


# p 1
encrypted_input = [(num, i)
                   for i, num in enumerate(get_encrypted_input())]
decoded_input = get_decoded_input(encrypted_input)
print(get_sum(decoded_input))

# p2
input = [(num * 811589153, i)
         for i, num in enumerate(get_encrypted_input())]

for _ in range(10):
    input = get_decoded_input(input)

print(get_sum(input))
