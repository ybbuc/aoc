def solve(input_text):
    tiles = []
    for line in input_text.strip().split('\n'):
        x, y = map(int, line.split(','))
        tiles.append((x, y))

    max_area = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            max_area = max(max_area, area)

    return max_area


if __name__ == "__main__":
    with open("input") as f:
        input_text = f.read()
    print(solve(input_text))
