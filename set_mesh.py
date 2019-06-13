X_WIDTH = [
    50, 50, 50, 50, 50, 50, 50,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    50, 50, 50, 50, 50, 50, 50,
]

Y_WIDTH = X_WIDTH.copy()


def generate_mesh():
    x_corner = [0]
    y_corner = [0]
    for x in X_WIDTH:
        x_corner.append(x_corner[-1] + x)
    for y in Y_WIDTH:
        y_corner.append(y_corner[-1] + y)
    x_center = [(x_corner[index] + x_corner[index + 1]) / 2 for index in range(len(X_WIDTH))]
    y_center = [(y_corner[index] + y_corner[index + 1]) / 2 for index in range(len(Y_WIDTH))]
    result = [(x, y) for y in y_center for x in x_center]
    return result
