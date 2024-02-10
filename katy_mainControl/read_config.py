config = {}

with open("../config") as file:
    for line in file:
        tmp = line.split("=")
        config[tmp[0]] = tmp[1].strip()
