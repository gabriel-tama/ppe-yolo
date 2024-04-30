def point_inside_rectangle(point, rectangle):
    """
    Check if a point is inside a rectangle.

    Parameters:
        point: Tuple (x, y) representing the coordinates of the point.
        rectangle: Tuple (x1, y1, x2, y2) representing the coordinates of the rectangle's top-left and bottom-right corners.

    Returns:
        True if the point is inside the rectangle, False otherwise.
    """
    x, y = point
    x1, y1, x2, y2 = rectangle

    if (x1 <= x <= x2) and (y1 <= y <= y2):
        return True
    else:
        return False

def rectangle_intersection(rect1, rect2):
    """
    Calculate the intersection area between two rectangles.

    Parameters:
        rect1: Tuple (x1, y1, x2, y2) representing the coordinates of the first rectangle's top-left and bottom-right corners.
        rect2: Tuple (x1, y1, x2, y2) representing the coordinates of the second rectangle's top-left and bottom-right corners.

    Returns:
        The area of the intersection between the two rectangles.
    """
    x1 = max(rect1[0], rect2[0])
    y1 = max(rect1[1], rect2[1])
    x2 = min(rect1[2], rect2[2])
    y2 = min(rect1[3], rect2[3])

    # Calculate the intersection area
    intersection_area = max(0, x2 - x1) * max(0, y2 - y1)
    return intersection_area


def most_intersections(rectangles):
    """
    Find the pair of rectangles with the most intersections.

    Parameters:
        rectangles: List of tuples representing the rectangles, each tuple in the format (x1, y1, x2, y2).

    Returns:
        The pair of rectangles with the most intersections, along with the number of intersections.
    """
    max_intersections = 0
    best_pair = None

    # Iterate over all pairs of rectangles
    for i in range(len(rectangles)):
        for j in range(i + 1, len(rectangles)):
            intersection_count = rectangle_intersection(rectangles[i], rectangles[j])

            # Update the best pair if the current pair has more intersections
            if intersection_count > max_intersections:
                max_intersections = intersection_count
                best_pair = (i, j)

    return best_pair, max_intersections
