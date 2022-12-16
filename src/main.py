from vex import *


brain = Brain()
controller = Controller()
left_wheel = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
right_wheel = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
back_wheel = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)

while True:
    drive = controller.axis3.position()
    turn = controller.axis1.position()
    lateral = controller.axis4.position()
    left_wheel_power = drive + turn
    right_wheel_power = drive - turn
    back_wheel_power = lateral
    back_wheel.spin(FORWARD, back_wheel_power, PERCENT)
    left_wheel.spin(FORWARD, left_wheel_power, PERCENT)
    right_wheel.spin(FORWARD, right_wheel_power, PERCENT)