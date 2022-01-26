s = "101101"
cells = []

for i, c in enumerate(s):
    if c == "1":
        cells.append(("input", i))

def and_reduce(cells):
    result = []
    i = 1
    while i < len(cells):
        result.append(("and", cells[i - 1], cells[i]))
        i += 2
    if i == len(cells):
        result.append(cells[i - 1])
    return result

while len(cells) > 1:
    cells = and_reduce(cells)

print(cells)
    
    