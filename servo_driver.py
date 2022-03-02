import RPi.GPIO as GPIO
import time
import math

SERVO_MIN = 2  # Duty cycle corresponding to 0° position of the servo
SERVO_MAX = 12  # Duty cycle corresponding to 180° position of the servo

# Cartesian coordinate limitations of the physical canvas
X_MIN = 10
Y_MIN = 10
X_MAX = 100
Y_MAX = 100

L1 = 92  # Shoulder to elbow distance
L2 = 85 # 119.5  # Elbow to hand distance
# Distance squared for readability and optimization
L1_sqr = L1**2
L2_sqr = L2**2


def initialize(shoulder_pin, elbow_pin, hand_pin):
    # Initialize GPIO pins and all PWMs
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(shoulder_pin, GPIO.OUT)
    GPIO.setup(elbow_pin, GPIO.OUT)
    GPIO.setup(hand_pin, GPIO.OUT)
    shoulder_pwm = GPIO.PWM(shoulder_pin, 50)
    elbow_pwm = GPIO.PWM(elbow_pin, 50)
    hand_pwm = GPIO.PWM(hand_pin, 50)
    # Start PWM signal
    shoulder_pwm.start(0)
    elbow_pwm.start(0)
    hand_pwm.start(0)
    time.sleep(0.1)
    # Move to initial position
    shoulder_pwm.ChangeDutyCycle(2)
    elbow_pwm.ChangeDutyCycle(2)
    hand_pwm.ChangeDutyCycle(5)
    time.sleep(0.3)
    # Stop the servos in initial position (prevents twitching)
    shoulder_pwm.ChangeDutyCycle(0)
    elbow_pwm.ChangeDutyCycle(0)
    hand_pwm.ChangeDutyCycle(0)  # pen is up
    return shoulder_pwm, elbow_pwm, hand_pwm  # Returns PWM objects to be used to control the servos


def cartesian_to_servo(x, y):
    # Check if coordinates are plottable
    assert 0 < x <= X_MAX - X_MIN
    assert 0 < y <= Y_MAX - Y_MIN
    # coordinates relative to first servo (rather than relative to bottom left of the canvas)
    x_ = x + X_MIN
    y_ = y + Y_MIN
    print(x_, y_)
    r_sqr = x_ ** 2 + y_ ** 2  # r^2 in polar coordinates
    alpha = math.atan(y_ / x_)  # angle in polar coordinates
    h = math.sqrt(L1_sqr - (r_sqr + L1_sqr - L2_sqr) ** 2 / (4 * r_sqr))  # height of the L1, L2, r triangle
    print(h)
    alpha_plus = math.asin(h / L1)
    beta_plus = math.asin(h / L2)
    theta = math.pi - (alpha + alpha_plus)  # shoulder servo angle
    phi = alpha_plus + beta_plus  # elbow servo angle
    print("theta:", theta, "phi:", phi)
    return theta, phi


def servo_to_dc(theta, phi):
    #  Map theta, phi from [0-pi] to [2-12]% SG90 duty cycle range
    shoulder_dc = theta*10/math.pi + 2
    elbow_dc = phi*10/math.pi + 2
    return shoulder_dc, elbow_dc


def points_to_instructions(points):
    instructions = []
    for point in points:
        theta, phi = cartesian_to_servo(point[0], point[1])
        sdc, edc = servo_to_dc(theta, phi)
        instructions.append([sdc, edc])
    print("instructions", instructions)
    return instructions


def plot_instructions(instructions, shoulder_pwm, elbow_pwm, hand_pwm):
    # move pen to first point
    shoulder_pwm.ChangeDutyCycle(instructions[0][0])
    elbow_pwm.ChangeDutyCycle(instructions[0][1])
    # Wait for movement completion
    time.sleep(0.3)
    # Prevents twitching
    shoulder_pwm.ChangeDutyCycle(0)
    elbow_pwm.ChangeDutyCycle(0)

    # move pen down
    hand_pwm.ChangeDutyCycle(7)
    time.sleep(0.5)  # Wait for pen to be down and steady

    for instruction in instructions[1:]:
        sdc = instruction[0]
        edc = instruction[1]
        # Move to new point
        shoulder_pwm.ChangeDutyCycle(sdc)
        elbow_pwm.ChangeDutyCycle(edc)
        # Wait for movement completion
        time.sleep(0.3)
        # Prevents twitching
        shoulder_pwm.ChangeDutyCycle(0)
        elbow_pwm.ChangeDutyCycle(0)

        time.sleep(3)

    # move pen up
    hand_pwm.ChangeDutyCycle(5)
    time.sleep(0.5)  # Wait for pen to be up


def stop_plot(shoulder_pwm, elbow_pwm, hand_pwm):
    # Move to initial position
    shoulder_pwm.ChangeDutyCycle(2)
    elbow_pwm.ChangeDutyCycle(2)
    hand_pwm.ChangeDutyCycle(2)
    time.sleep(0.3)
    # Stop the servos in initial position (prevents twitching)
    shoulder_pwm.ChangeDutyCycle(0)
    elbow_pwm.ChangeDutyCycle(0)
    hand_pwm.ChangeDutyCycle(0)  # pen is up

    # Stop PWMs
    shoulder_pwm.stop()
    elbow_pwm.stop()
    hand_pwm.stop()

    # Clear GPIO
    GPIO.cleanup()

