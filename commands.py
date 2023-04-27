# Serial commands
class Command:
    ANALOG_READ = 'a'
    GET_BAUDRATE = 'b'
    PIN_MODE = 'c'
    DIGITAL_READ = 'd'
    READ_ENCODERS = 'e'
    MOTOR_SPEEDS = 'm'
    MOTOR_RAW_PWM = 'o'
    PING = 'p'
    RESET_ENCODERS = 'r'
    SERVO_WRITE = 's'
    SERVO_READ = 't'
    UPDATE_PID = 'u'
    DIGITAL_WRITE = 'w'
    ANALOG_WRITE = 'x'

# Direction
class Direction:
    LEFT = 0
    RIGHT = 1
