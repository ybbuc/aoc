import bisect


def solve(input_text):
    # Parse red tiles (vertices of the polygon in order)
    tiles = []
    for line in input_text.strip().split('\n'):
        x, y = map(int, line.split(','))
        tiles.append((x, y))

    n = len(tiles)

    # Build segments of the polygon (consecutive tiles connected)
    # Separate into horizontal and vertical, with normalized coords
    h_segments = []  # (y, x_min, x_max)
    v_segments = []  # (x, y_min, y_max)

    for i in range(n):
        x1, y1 = tiles[i]
        x2, y2 = tiles[(i + 1) % n]
        if x1 == x2:  # vertical
            v_segments.append((x1, min(y1, y2), max(y1, y2)))
        else:  # horizontal
            h_segments.append((y1, min(x1, x2), max(x1, x2)))

    # Sort for binary search
    # v_segments sorted by x, h_segments sorted by y
    v_segments.sort()
    h_segments.sort()
    v_xs = [s[0] for s in v_segments]
    h_ys = [s[0] for s in h_segments]

    def point_in_polygon(px, py):
        """Ray casting algorithm - count crossings to the right"""
        crossings = 0
        # Only check vertical segments with x > px
        start = bisect.bisect_right(v_xs, px)
        for i in range(start, len(v_segments)):
            x, y_min, y_max = v_segments[i]
            if y_min < py < y_max:
                crossings += 1
        return crossings % 2 == 1

    def point_on_boundary(px, py):
        """Check if point is on the polygon boundary"""
        # Check vertical segments at x == px
        idx = bisect.bisect_left(v_xs, px)
        while idx < len(v_segments) and v_segments[idx][0] == px:
            x, y_min, y_max = v_segments[idx]
            if y_min <= py <= y_max:
                return True
            idx += 1

        # Check horizontal segments at y == py
        idx = bisect.bisect_left(h_ys, py)
        while idx < len(h_segments) and h_segments[idx][0] == py:
            y, x_min, x_max = h_segments[idx]
            if x_min <= px <= x_max:
                return True
            idx += 1

        return False

    def point_inside_or_on(px, py):
        """Check if point is inside or on boundary of polygon"""
        return point_in_polygon(px, py) or point_on_boundary(px, py)

    def any_segment_crosses_rect_interior(left, right, bottom, top):
        """
        Check if any polygon segment crosses through the interior of the
        rectangle (not just touching the boundary).
        """
        # Check vertical segments with x strictly between left and right
        lo = bisect.bisect_right(v_xs, left)
        hi = bisect.bisect_left(v_xs, right)
        for i in range(lo, hi):
            x, y_min, y_max = v_segments[i]
            # x is strictly inside (left < x < right)
            # Check if segment's y range overlaps with (bottom, top)
            if y_min < top and y_max > bottom:
                return True

        # Check horizontal segments with y strictly between bottom and top
        lo = bisect.bisect_right(h_ys, bottom)
        hi = bisect.bisect_left(h_ys, top)
        for i in range(lo, hi):
            y, x_min, x_max = h_segments[i]
            # y is strictly inside (bottom < y < top)
            # Check if segment's x range overlaps with (left, right)
            if x_min < right and x_max > left:
                return True

        return False

    def rectangle_valid(rx1, ry1, rx2, ry2):
        """
        Check if rectangle with corners (rx1,ry1) and (rx2,ry2)
        is fully inside polygon.
        """
        # Check all 4 corners are inside or on polygon
        corners = [(rx1, ry1), (rx1, ry2), (rx2, ry1), (rx2, ry2)]
        for cx, cy in corners:
            if not point_inside_or_on(cx, cy):
                return False

        # Check no polygon segment crosses through the interior
        left, right = min(rx1, rx2), max(rx1, rx2)
        bottom, top = min(ry1, ry2), max(ry1, ry2)
        if any_segment_crosses_rect_interior(left, right, bottom, top):
            return False

        return True

    # Try all pairs of red tiles as opposite corners
    max_area = 0
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]

            # Skip if same row or column
            if x1 == x2 or y1 == y2:
                continue

            if rectangle_valid(x1, y1, x2, y2):
                area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
                max_area = max(max_area, area)

    return max_area


if __name__ == "__main__":
    with open("input") as f:
        input_text = f.read()
    print(solve(input_text))
