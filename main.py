import json


def findValue(data):
    minValue = 9999999999
    for element in data:
        value = data[element]["cps"] / data[element]["cost"]
        data[element]["value"] = value
        minValue = min(minValue, value)
    for element in data:
        data[element]["value"] = data[element]["value"] / minValue
    return data


def displayStats(data):
    findValue(data)
    print("--------------------------------")
    for element in data:
        print(element)
        for stat in data[element]:
            print(f"  {stat}: {data[element][stat]}")
    print("--------------------------------")
    return data


def save(data):
    with open("data.json", "w") as write_file:
            json.dump(data, write_file)

data = {}

with open("data.json", "r") as read_file:
    data = json.load(read_file)

while True:
    s = input()
    if s == 'exit':
        save(data)
        break
    if s == 'display':
        data = displayStats(data)
    if "+" in s:
        a, n, building = s.split()
        data[building]["n"] += int(n)
        data[building]["cost"] = int(data[building]["cost"] * 1.15 ** int(n))

        save(data)
        data = displayStats(data)
    if "cps" in s:
        a, building, cps = s.split()
        data[building]["cps"] = float(cps)

        save(data)
        data = displayStats(data)
    if "cost" in s:
        a, building, cost = s.split()
        data[building]["cost"] = int(cost)

        save(data)
        data = displayStats(data)
