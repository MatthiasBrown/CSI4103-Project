import time
import servo_driver as sd

SHOULDER_PIN = 13
ELBOW_PIN = 19
HAND_PIN = 26


def main():
    s_pwm, e_pwm, h_pwm = sd.initialize(SHOULDER_PIN, ELBOW_PIN, HAND_PIN)
    line = [[15, 35], [15, 85], [85, 85], [85, 35], [15, 35]]  # Draws a square
    instructions = sd.points_to_instructions(line)  # Generate instructions
    sd.plot_instructions(instructions, s_pwm, e_pwm, h_pwm)  # Plots instructions
    time.sleep(2)
    sd.stop_plot(s_pwm, e_pwm, h_pwm)  # Stop the plotter


if __name__ == "__main__":
    main()
