from vex import *

INTAKE_VELOCITY = 100
TURN_SENSIBILITY = 0.6
CATAPULT_POWER = 80

brain = Brain()
controller = Controller()
left_wheel = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)
right_wheel = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
back_wheel = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
intake = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
roller = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
catapult = Motor(Ports.PORT6, GearSetting.RATIO_18_1,True)
#catapult_stopper = Bumper(Triport.a, brain = brain)

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

l1_was_clicked = False
r1_was_clicked = False
def user_control():
    global l1_was_clicked
    global r1_was_clicked
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

        if l1_was_clicked and not controller.buttonL1.pressing():
            control_intake(1)
        if r1_was_clicked and not controller.buttonR1.pressing():
            control_intake(-1)

        if controller.buttonY.pressing(): 
            catapult.spin(FORWARD, CATAPULT_POWER, PERCENT)

        l1_was_clicked = controller.buttonL1.pressing()
        r1_was_clicked = controller.buttonR1.pressing()

def joystick_smoother(joystick_axis: float):
    return 1.2 * math.tan(0.7 * joystick_axis)

def control_intake(direction: int):
    current_direction = intake.velocity(PERCENT) // INTAKE_VELOCITY
    if current_direction != 0:
        intake.set_velocity(0)
    elif direction > 0:
        intake.set_velocity(INTAKE_VELOCITY)
    else:
        intake.set_velocity(-INTAKE_VELOCITY)

def catapult_stop(bumper_act):
    """if catapult_stopper == 1:
        catapult.set_velocity(0, PERCENT)
    else:
        pass"""

comp = Competition(user_control, autonomous)
pre_autonomous()