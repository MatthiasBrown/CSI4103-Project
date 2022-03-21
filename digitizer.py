import numpy as np
from math import cos, sin
from matplotlib import pyplot as plt


# Translates 300 degrees potentiometer 10 bit data to radians
def analog_to_radian(inp):
    return (1 - (inp/1023))*(5/3)*np.pi


# Translates Brachiograph angles in radians into cartesian coordinates
def angles_to_coords(theta, phi, l1, l2):
    x = -l1 * cos(theta) - l2 * cos(theta + phi)
    y = l1 * sin(theta) + l2 * sin(theta + phi)
    return [x, y]


# Takes a list of 2 element lists of 10 bit potentiometer data, returns a list of x, y coordinates
def digitize(list_of_inputs, l1, l2):
    angles = []
    for inp in list_of_inputs:
        angles.append([analog_to_radian(inp[0]), analog_to_radian(inp[1])])
    coord = []
    print(angles)
    for ang in angles:
        coord.append(angles_to_coords(ang[0], ang[1], l1, l2))
    return coord


def plot_digitized(coord):
    coord_x = [c[0] for c in coord]
    coord_y = [c[1] for c in coord]
    plt.plot(coord_x, coord_y)
    plt.show()


def main():
    l1 = 98
    l2 = 125  # Real prototype lengths
    list_of_inputs = [[600, 1020], [550, 900], [400, 800], [250, 600], [50, 500]]
    coord = digitize(list_of_inputs, l1, l2)
    print(coord)
    plot_digitized(coord)


if __name__ == "__main__":
    main()
