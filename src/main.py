from vex import *

INTAKE_VELOCITY = 100
TURN_SENSIBILITY = 0.6
CATAPULT_POWER = 80

brain = Brain()
controller = Controller()
left_wheel = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
right_wheel = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
back_wheel = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
roller = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)
catapult= Motor(Ports.PORT8, GearSetting.RATIO_18_1,True)


def pre_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("pre auton code")
    wait(1, SECONDS)

def autonomous():
    """brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    # place automonous code here
    left_wheel.spin_to_position(100, rotationUnits=RotationUnits.DEG, velocity=None, velocityUnits=VelocityUnits.PCT, waitForCompletion=True)
    right_wheel.spin_to_position(100, rotationUnits=RotationUnits.DEG, velocity=None, velocityUnits=VelocityUnits.PCT, waitForCompletion=True)
    wait(1, SECONDS)"""

def user_control():
    brain.screen.clear_screen()
    while True:    
        drive = joystick_smoother(controller.axis3.position())
        turn = joystick_smoother(controller.axis1.position()) * TURN_SENSIBILITY
        lateral = joystick_smoother(controller.axis4.position())
        left_wheel_power = drive + turn
        right_wheel_power = drive - turn
        back_wheel_power = lateral
        back_wheel.spin(FORWARD, back_wheel_power, PERCENT)
        left_wheel.spin(FORWARD, left_wheel_power, PERCENT)
        right_wheel.spin(FORWARD, right_wheel_power, PERCENT)

        if controller.buttonL2.pressing():
            intake.spin(FORWARD, INTAKE_VELOCITY, PERCENT)
        elif controller.buttonR2.pressing():
            intake.spin(REVERSE, INTAKE_VELOCITY, PERCENT)
        else:
            intake.set_velocity(0, PERCENT)

        if controller.buttonY.pressing(): 
            catapult.spin(FORWARD, CATAPULT_POWER, PERCENT)

def joystick_smoother(joystick_axis: float):
    return 1.2 * math.tan(0.7 * joystick_axis)


comp = Competition(user_control, autonomous)
pre_autonomous()