import numpy as np


def generate_mindlin_stiffness_matrix(x_list, y_list, modulus_of_elasticity=30E6, poisson=0.5, depth=50):
    length = len(x_list)

    x_list = x_list.reshape(length ** 2)
    y_list = y_list.reshape(length ** 2)

    result = np.ones((44 * 44, 44 * 44))
    result *= ((1 + poisson) / np.pi / modulus_of_elasticity)

    for force_index in range(length ** 2):
        for displacement_index in range(force_index, length ** 2):
            x1 = x_list[force_index]
            y1 = y_list[force_index]
            x2 = x_list[displacement_index]
            y2 = y_list[displacement_index]
            r = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + depth ** 2)
            result[force_index, displacement_index] *= ((1 - poisson + depth ** 2 / 2 / r ** 2) / r)
            result[displacement_index, force_index] *= ((1 - poisson + depth ** 2 / 2 / r ** 2) / r)
    return result


def generate_boussinesq_stiffness_matrix(
        x_list, y_list, a_list, b_list, modulus_of_elasticity=30E6, poisson=0.5, depth=50):
    length = len(x_list)

    x_list = x_list.reshape(length ** 2)
    y_list = y_list.reshape(length ** 2)
    a_list = a_list.reshape(length ** 2)
    b_list = b_list.reshape(length ** 2)

    result = np.ones((length * length, length * length))

    for force_index in range(length ** 2):
        for displacement_index in range(force_index + 1, length ** 2):
            x1 = x_list[force_index]
            y1 = y_list[force_index]
            x2 = x_list[displacement_index]
            y2 = x_list[displacement_index]
            r = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + depth ** 2)
            result[force_index, displacement_index] *= ((1 - poisson + depth ** 2 / 2 / r ** 2) / r)
            result[displacement_index, force_index] *= ((1 - poisson + depth ** 2 / 2 / r ** 2) / r)
    return result


if __name__ == '__main__':
    print(generate_mindlin_stiffness_matrix(
        x_list=np.asarray([2, 5, 2, 5]).reshape((2, 2)),
        y_list=np.asarray([2, 2, 5, 5]).reshape((2, 2)),
    ))
