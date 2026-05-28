import tkinter as tk

kp = 5.0
ki = 0.01
kd = 0.5

servo_1_angle = 90
servo_2_angle = 90
servo_3_angle = 90

max_pwm = 80
motor_start_pwm = 20
pid_output_limit = 60

def send_to_pico(command): # Placeholder function to send command to Pico
    print("Sending:", command)

def clamp(value, minimum, maximum):  # Utility function to clamp a value between a minimum and maximum
    return max(minimum, min(maximum, value))

def update_label(label, name, value): # Utility function to update a label with the current value of a setting
    label.config(text=f"{name}: {value}")

def change_pid(name, amount, label): # Function to change PID values and send command to Pico, with name indicating which PID parameter to change and amount indicating how much to change it by, and label being the label to update with the new value
    global kp, ki, kd

    if name == "Kp": 
        kp = round(kp + amount, 4)
        value = kp
        command = f"kp {kp}"
    elif name == "Ki":
        ki = round(ki + amount, 4)
        value = ki
        command = f"ki {ki}"
    elif name == "Kd":
        kd = round(kd + amount, 4)
        value = kd
        command = f"kd {kd}"

    update_label(label, name, value)
    send_to_pico(command)

def change_servo(servo_number, amount, label):
    global servo_1_angle, servo_2_angle, servo_3_angle

    if servo_number == 1:
        servo_1_angle = clamp(servo_1_angle + amount, 0, 180)
        angle = servo_1_angle
    elif servo_number == 2:
        servo_2_angle = clamp(servo_2_angle + amount, 0, 180)
        angle = servo_2_angle
    else:
        servo_3_angle = clamp(servo_3_angle + amount, 0, 180)
        angle = servo_3_angle

    label.config(text=f"Servo {servo_number}: {angle} degrees")
    send_to_pico(f"servo {servo_number} {angle}")

def set_servo(servo_number, angle, label):
    global servo_1_angle, servo_2_angle, servo_3_angle

    angle = clamp(angle, 0, 180)

    if servo_number == 1:
        servo_1_angle = angle
    elif servo_number == 2:
        servo_2_angle = angle
    else:
        servo_3_angle = angle

    label.config(text=f"Servo {servo_number}: {angle} degrees")
    send_to_pico(f"servo {servo_number} {angle}")

def change_motor_setting(setting_name, amount, label):
    global max_pwm, motor_start_pwm, pid_output_limit

    if setting_name == "max_pwm":
        max_pwm = clamp(max_pwm + amount, 0, 100)
        value = max_pwm
        command = f"motor maxpwm {value}"

    elif setting_name == "motor_start_pwm":
        motor_start_pwm = clamp(motor_start_pwm + amount, 0, max_pwm)
        value = motor_start_pwm
        command = f"motor startpwm {value}"

    elif setting_name == "pid_output_limit":
        pid_output_limit = clamp(pid_output_limit + amount, 1, 1000)
        value = pid_output_limit
        command = f"motor pidlimit {value}"

    update_label(label, setting_name, value)
    send_to_pico(command)

window = tk.Tk()
window.title("Robot Control Panel")
window.geometry("900x500")

main_frame = tk.Frame(window)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

pid_frame = tk.LabelFrame(main_frame, text="PID Settings", padx=10, pady=10)
pid_frame.grid(row=0, column=0, sticky="nsew", padx=5)

servo_frame = tk.LabelFrame(main_frame, text="Servo Control", padx=10, pady=10)
servo_frame.grid(row=0, column=1, sticky="nsew", padx=5)

motor_frame = tk.LabelFrame(main_frame, text="Motor Settings", padx=10, pady=10)
motor_frame.grid(row=0, column=2, sticky="nsew", padx=5)

main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)

# PID buttons
kp_label = tk.Label(pid_frame, text=f"Kp: {kp}")
kp_label.pack(pady=5)
tk.Button(pid_frame, text="- Kp", width=18, command=lambda: change_pid("Kp", -0.1, kp_label)).pack()
tk.Button(pid_frame, text="+ Kp", width=18, command=lambda: change_pid("Kp", 0.1, kp_label)).pack()

ki_label = tk.Label(pid_frame, text=f"Ki: {ki}")
ki_label.pack(pady=5)
tk.Button(pid_frame, text="- Ki", width=18, command=lambda: change_pid("Ki", -0.01, ki_label)).pack()
tk.Button(pid_frame, text="+ Ki", width=18, command=lambda: change_pid("Ki", 0.01, ki_label)).pack()

kd_label = tk.Label(pid_frame, text=f"Kd: {kd}")
kd_label.pack(pady=5)
tk.Button(pid_frame, text="- Kd", width=18, command=lambda: change_pid("Kd", -0.1, kd_label)).pack()
tk.Button(pid_frame, text="+ Kd", width=18, command=lambda: change_pid("Kd", 0.1, kd_label)).pack()

# Servo buttons
servo1_label = tk.Label(servo_frame, text=f"Servo 1: {servo_1_angle} degrees")
servo1_label.pack(pady=5)
tk.Button(servo_frame, text="- Servo 1", width=18, command=lambda: change_servo(1, -1, servo1_label)).pack()
tk.Button(servo_frame, text="+ Servo 1", width=18, command=lambda: change_servo(1, 1, servo1_label)).pack()
tk.Button(servo_frame, text="Servo 1 to 90", width=18, command=lambda: set_servo(1, 90, servo1_label)).pack()

servo2_label = tk.Label(servo_frame, text=f"Servo 2: {servo_2_angle} degrees")
servo2_label.pack(pady=5)
tk.Button(servo_frame, text="- Servo 2", width=18, command=lambda: change_servo(2, -1, servo2_label)).pack()
tk.Button(servo_frame, text="+ Servo 2", width=18, command=lambda: change_servo(2, 1, servo2_label)).pack()
tk.Button(servo_frame, text="Servo 2 to 90", width=18, command=lambda: set_servo(2, 90, servo2_label)).pack()

servo3_label = tk.Label(servo_frame, text=f"Servo 3: {servo_3_angle} degrees")
servo3_label.pack(pady=5)
tk.Button(servo_frame, text="- Servo 3", width=18, command=lambda: change_servo(3, -1, servo3_label)).pack()
tk.Button(servo_frame, text="+ Servo 3", width=18, command=lambda: change_servo(3, 1, servo3_label)).pack()
tk.Button(servo_frame, text="Servo 3 to 90", width=18, command=lambda: set_servo(3, 90, servo3_label)).pack()

# Motor buttons
max_pwm_label = tk.Label(motor_frame, text=f"max_pwm: {max_pwm}")
max_pwm_label.pack(pady=5)
tk.Button(motor_frame, text="- maxPWM", width=22, command=lambda: change_motor_setting("max_pwm", -1, max_pwm_label)).pack()
tk.Button(motor_frame, text="+ maxPWM", width=22, command=lambda: change_motor_setting("max_pwm", 1, max_pwm_label)).pack()

motor_start_pwm_label = tk.Label(motor_frame, text=f"motor_start_pwm: {motor_start_pwm}")
motor_start_pwm_label.pack(pady=5)
tk.Button(motor_frame, text="- motorStartPWM", width=22, command=lambda: change_motor_setting("motor_start_pwm", -1, motor_start_pwm_label)).pack()
tk.Button(motor_frame, text="+ motorStartPWM", width=22, command=lambda: change_motor_setting("motor_start_pwm", 1, motor_start_pwm_label)).pack()

pid_output_limit_label = tk.Label(motor_frame, text=f"pid_output_limit: {pid_output_limit}")
pid_output_limit_label.pack(pady=5)
tk.Button(motor_frame, text="- PID Output Limit", width=22, command=lambda: change_motor_setting("pid_output_limit", -1, pid_output_limit_label)).pack()
tk.Button(motor_frame, text="+ PID Output Limit", width=22, command=lambda: change_motor_setting("pid_output_limit", 1, pid_output_limit_label)).pack()

# General buttons at bottom
general_frame = tk.LabelFrame(window, text="General", padx=10, pady=10)
general_frame.pack(fill="x", padx=10, pady=10)

tk.Button(general_frame, text="Start PID", width=15, command=lambda: send_to_pico("pid start")).pack(side="left", padx=5)
tk.Button(general_frame, text="Stop PID", width=15, command=lambda: send_to_pico("pid stop")).pack(side="left", padx=5)
tk.Button(general_frame, text="FORCE STOP", width=15, command=lambda: send_to_pico("FORCE")).pack(side="left", padx=5)

window.mainloop()