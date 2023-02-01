from vex import *


brain = Brain()
controller = Controller()
left_wheel = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
right_wheel = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
back_wheel = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)
intake = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
above_wheel = Motor(Ports.PORT13, GearSetting.RATIO_18_1, True)
Catapulta= Motor(Ports.PORT8, GearSetting.RATIO_18_1,True)
Loop= 1
INTAKE_VELOCITY = 100
TURN_SENSIBILITY = 0.6
OUTTAKE_VELOCITY = 40

while True:
    drive = controller.axis3.position()
    turn = controller.axis1.position() * TURN_SENSIBILITY
    lateral = controller.axis4.position()
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

    if controller.buttonL1.pressing():
        above_wheel.spin(FORWARD, INTAKE_VELOCITY, PERCENT)
    elif controller.buttonR1.pressing():
        above_wheel.spin(REVERSE, INTAKE_VELOCITY, PERCENT)
    else:
        above_wheel.set_velocity(0, PERCENT)

    if controller.buttonY.pressing(): 
        Catapulta.spin(FORWARD, OUTTAKE_VELOCITY, PERCENT)
    elif controller.buttonA.pressing():
        Catapulta.spin(REVERSE, OUTTAKE_VELOCITY, PERCENT)
    else:
        Catapulta.set_velocity(0, PERCENT)
