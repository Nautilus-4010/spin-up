import time
from vex import *

INTAKE_VELOCITY = 100
TURN_SENSIBILITY = 0.5
LATERAL_SENSIBILITY = 0.6
CATAPULT_POWER = 80


brain = Brain()
controller = Controller()
left_wheel = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
right_wheel = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
back_wheel = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
intake = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
roller = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
catapult = Motor(Ports.PORT6, GearSetting.RATIO_18_1,True)
catapult_stop = Bumper(brain.three_wire_port.a)

def pre_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("pre auton code")
    wait(1, SECONDS)

def autonomous():
    catapult.reset_position()
    catapult.spin_to_position(360, DEGREES, INTAKE_VELOCITY)
    while catapult.is_spinning():
        time.sleep(0.1)

is_shooting = False
l1_was_clicked = False
r1_was_clicked = False
was_a_clicked = False
def user_control():
    global is_shooting
    global was_a_clicked
    global l1_was_clicked
    global r1_was_clicked
    brain.screen.clear_screen()
    while True:    
        drive = joystick_smoother(controller.axis3.position())
        turn = joystick_smoother(controller.axis1.position()) * TURN_SENSIBILITY
        lateral = joystick_smoother(controller.axis4.position()) * LATERAL_SENSIBILITY
        left_wheel_power = drive + turn
        right_wheel_power = drive - turn
        back_wheel_power = lateral
        max_velocity = max(abs(back_wheel_power), max(abs(left_wheel_power), abs(right_wheel_power)))
        power_multiplier = 0.85
        if max_velocity > 1:
            left_wheel_power /= max_velocity
            right_wheel_power /= max_velocity
            back_wheel_power /= max_velocity
        if controller.buttonR2.pressing() and controller.buttonL2.pressing():
            power_multiplier = 1
        
        back_wheel_power *= 100 * power_multiplier
        left_wheel_power *= 100 * power_multiplier
        right_wheel_power *= 100 * power_multiplier
        back_wheel.spin(FORWARD, back_wheel_power, PERCENT)
        left_wheel.spin(FORWARD, left_wheel_power, PERCENT)
        right_wheel.spin(FORWARD, right_wheel_power, PERCENT)

        if controller.buttonY.pressing():
            roller.spin(FORWARD, 100, PERCENT)
        elif controller.buttonA.pressing():
            roller.spin(REVERSE, 100, PERCENT)
        else:
            roller.set_velocity(0, PERCENT)

        if l1_was_clicked and not controller.buttonL1.pressing():
            control_intake(1)
        if r1_was_clicked and not controller.buttonR1.pressing():
            control_intake(-1)

        if was_a_clicked and not controller.buttonA.pressing():
            is_shooting = True
        if controller.buttonX.pressing():
            catapult.set_velocity(CATAPULT_POWER, PERCENT)
        elif controller.buttonB.pressing():
            catapult.set_velocity(-CATAPULT_POWER, PERCENT)
        else:
            catapult.set_velocity(0)
        catapult.spin(FORWARD)

        catapult_control()
        l1_was_clicked = controller.buttonL1.pressing()
        r1_was_clicked = controller.buttonR1.pressing()
        time.sleep(0.1)

def joystick_smoother(joystick_axis: float):
    return 1.2 * math.tan(0.7 * joystick_axis / 100)

def control_intake(direction: int):
    if intake.velocity(PERCENT) != 0:
        intake.set_velocity(0)
    elif direction > 0:
        intake.spin(FORWARD, INTAKE_VELOCITY, PERCENT)
    else:
        intake.spin(REVERSE, INTAKE_VELOCITY, PERCENT)

def catapult_control():
    global is_shooting
    bumper_pressed = catapult_stop.pressing()
    if is_shooting and bumper_pressed:
        print("Move motor")
    elif is_shooting and not bumper_pressed:
        is_shooting = False
    elif not is_shooting and bumper_pressed:
        print("Stop intake")
    else:
        print("Move motor")

comp = Competition(user_control, autonomous)
pre_autonomous()