from matplotlib import pyplot as plt
import math

X_MIN = 0
X_MAX = 100
Y_MIN = 0
Y_MAX = 100

L1 = 30  # Shoulder to elbow distance
L2 = 40  # 119.5  # Elbow to hand distance
# Distance squared for readability and optimization
L1_sqr = L1**2
L2_sqr = L2**2


def cartesian_to_servo(x, y):
    # Check if coordinates are plottable
    assert 0 < x <= X_MAX - X_MIN
    assert 0 < y <= Y_MAX - Y_MIN
    # coordinates relative to first servo (rather than relative to bottom left of the canvas)
    x_ = x + X_MIN
    y_ = y + Y_MIN
    print(x_, y_)
    r_sqr = x_**2 + y_**2  # r^2 in polar coordinates
    alpha = math.atan(y_/x_)  # angle in polar coordinates
    h = math.sqrt(L1_sqr - (r_sqr + L1_sqr - L2_sqr)**2/(4 * r_sqr))  # height of the L1, L2, r triangle
    print(h)
    alpha_plus = math.asin(h/L1)
    beta_plus = math.asin(h/L2)
    theta = math.pi - (alpha + alpha_plus)  # shoulder servo angle
    phi = alpha_plus + beta_plus  # elbow servo angle
    print("theta:", theta, "phi:", phi)
    return theta, phi


def servo_to_cartesian(theta, phi):
    x = -L1*math.cos(theta) - L2*math.cos(theta + phi)
    y = L1*math.sin(theta) + L2*math.sin(theta + phi)
    return x, y


def servo_to_elbow(theta):
    x = -L1*math.cos(theta)
    y = L1*math.sin(theta)
    return x, y


target_x = 10
target_y = 5

t, h = cartesian_to_servo(target_x, target_y)
xe, ye = servo_to_elbow(t)
x, y = servo_to_cartesian(t, h)
print(x, y)

plt.plot([0, xe, x], [0, ye, y])
plt.plot(target_x + X_MIN, target_y + Y_MIN, "ro")
plt.show()
