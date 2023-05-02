# For L298_MOTOR_DRIVER
from machine import Pin, PWM

MAX_PWM = 255

RIGHT_MOTOR_BACKWARD = 5
LEFT_MOTOR_BACKWARD = 6
RIGHT_MOTOR_FORWARD = 9
LEFT_MOTOR_FORWARD = 10
RIGHT_MOTOR_ENABLE = 12
LEFT_MOTOR_ENABLE = 13

class MotorL298:
    LOW = 0
    HIGH = 1
    FREQ = 1000

    def __init__(self, forward, backward, enable):
        self.forward_pin = PWM(Pin(forward))
        self.forward_pin.freq(self.FREQ)
        self.backward_pin = PWM(Pin(backward))
        self.backward_pin.freq(self.FREQ)
        self.enable_pin = Pin(enable, Pin.OUT)
        self.enable_pin.value(self.HIGH)

    def set_speed(self, speed):
        reverse = 0
        if speed < 0:
            speed = -speed
            reverse = 1
        if speed > 255:
            speed = 255
        if reverse == 0:
            self.forward_pin.duty_u16(speed)
            self.backward_pin.duty_u16(0)
        elif reverse == 1:
            self.forward_pin.duty_u16(0)
            self.backward_pin.duty_u16(speed)

leftMotor = MotorL298(LEFT_MOTOR_FORWARD, LEFT_MOTOR_BACKWARD, LEFT_MOTOR_ENABLE)
rightMotor = MotorL298(RIGHT_MOTOR_FORWARD, RIGHT_MOTOR_BACKWARD, RIGHT_MOTOR_ENABLE)

def set_motor_speeds(left, right):
    leftMotor.set_speed(left)
    rightMotor.set_speed(right)