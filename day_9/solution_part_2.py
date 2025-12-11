def solve(input_text):
    # Parse red tiles (vertices of the polygon in order)
    tiles = []
    for line in input_text.strip().split('\n'):
        x, y = map(int, line.split(','))
        tiles.append((x, y))

    n = len(tiles)

    # Build segments of the polygon (consecutive tiles connected)
    # Each segment is either horizontal (same y) or vertical (same x)
    segments = []
    for i in range(n):
        x1, y1 = tiles[i]
        x2, y2 = tiles[(i + 1) % n]
        segments.append(((x1, y1), (x2, y2)))

    def point_in_polygon(px, py):
        """Ray casting algorithm - count crossings to the right"""
        crossings = 0
        for (x1, y1), (x2, y2) in segments:
            if x1 == x2:  # vertical segment
                # Check if horizontal ray from (px, py) going
                # right crosses this segment
                if x1 > px:  # segment is to the right
                    min_y, max_y = min(y1, y2), max(y1, y2)
                    if min_y < py < max_y:  # ray crosses (not touching endpoints)
                        crossings += 1
            # horizontal segments don't count as crossings for a horizontal ray
        return crossings % 2 == 1

    def point_on_boundary(px, py):
        """Check if point is on the polygon boundary"""
        for (x1, y1), (x2, y2) in segments:
            if x1 == x2:  # vertical segment
                if px == x1 and min(y1, y2) <= py <= max(y1, y2):
                    return True
            else:  # horizontal segment
                if py == y1 and min(x1, x2) <= px <= max(x1, x2):
                    return True
        return False

    def point_inside_or_on(px, py):
        """Check if point is inside or on boundary of polygon"""
        return point_in_polygon(px, py) or point_on_boundary(px, py)

    def segment_crosses_rect_interior(seg, rx1, ry1, rx2, ry2):
        """
        Check if a polygon segment crosses through the interior of the
        rectangle (not just touching the boundary).

        rx1, ry1 is one corner, rx2, ry2 is opposite corner.
        """
        (sx1, sy1), (sx2, sy2) = seg

        # Normalize rectangle bounds
        left = min(rx1, rx2)
        right = max(rx1, rx2)
        bottom = min(ry1, ry2)
        top = max(ry1, ry2)

        if sx1 == sx2:  # vertical segment
            x = sx1
            seg_bottom = min(sy1, sy2)
            seg_top = max(sy1, sy2)

            # Segment must be strictly inside x bounds (not on edge)
            if left < x < right:
                # Check if segment's y range overlaps with rectangle's y range
                if seg_bottom < top and seg_top > bottom:
                    return True
        else:  # horizontal segment (sy1 == sy2)
            y = sy1
            seg_left = min(sx1, sx2)
            seg_right = max(sx1, sx2)

            # Segment must be strictly inside y bounds (not on edge)
            if bottom < y < top:
                # Check if segment's x range overlaps with rectangle's x range
                if seg_left < right and seg_right > left:
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
        for seg in segments:
            if segment_crosses_rect_interior(seg, rx1, ry1, rx2, ry2):
                return False

        return True

    # Try all pairs of red tiles as opposite corners
    max_area = 0
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]

            # Skip if same row or column (area would be a line,
            # not really meaningful but let's include)
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
