import math
f = open("data.txt")


def calculate_operation(op_str, item):
    return eval(op_str.replace("old", str(item)))


def read_monkeys():
    monkeys = {}
    current_monkey = None
    for l in f.readlines():
        l = l.strip()

        if l.startswith("Monkey"):
            monkey_str = l.split(" ")[1][:-1]
            current_monkey = int(monkey_str)
            monkeys[current_monkey] = {"total_inspections": 0}
            continue

        if current_monkey == None:
            continue

        if l.startswith("Starting items"):
            monkeys[current_monkey]["items"] = [
                int(x.strip()) for x in l.split(":")[1].split(",")]

        elif l.startswith("Operation"):
            operation_str = l.split("=")[1]
            monkeys[current_monkey]["operation"] = operation_str
        elif l.startswith("Test"):
            divisible_by = int(l.split(" ")[-1:][0])
            monkeys[current_monkey]["divisible_by"] = divisible_by
        elif l.startswith("If true"):
            monkey_to_throw = int(l.split(" ")[-1:][0])
            monkeys[current_monkey]["true"] = monkey_to_throw
        elif l.startswith("If false"):
            monkey_to_throw = int(l.split(" ")[-1:][0])
            monkeys[current_monkey]["false"] = monkey_to_throw
        else:
            current_monkey = None

    return monkeys


monkeys = read_monkeys()
rounds = 10000  # 20 for p1
divisble_by_prod = math.prod([m["divisible_by"] for m in monkeys.values()])

for r in range(rounds):
    # print("##### ROUND " + str(r + 1) + "\n")
    for i in range(len(monkeys)):
        monkey = monkeys[i]
        items = monkey["items"]
        for item in items:
            monkey["total_inspections"] += 1
            item_after_op = calculate_operation(monkey["operation"], item)
            # item_after_divided = int(item_after_op / 3) for p1
            item_after_divided = item_after_op % divisble_by_prod
            is_divisible = item_after_op % monkey["divisible_by"] == 0
            next_monkey = monkey["true"] if is_divisible else monkey["false"]
            monkeys[next_monkey]["items"].append(item_after_divided)

        monkeys[i]["items"] = []


items = [m["total_inspections"] for x, m in monkeys.items()]
max1 = max(items)
items.remove(max1)
max2 = max(items)
print(max1 * max2)
