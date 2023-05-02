# Functions and type-defs for PID control.
# Taken mostly from Mike Ferguson's ArbotiX code which lives at:
# http://vanadium-ros-pkg.googlecode.com/svn/trunk/arbotix/
from drivers.encoder import read_encoder, LEFT_ENCODER, RIGHT_ENCODER
from drivers.motor import set_motor_speeds, MAX_PWM

# PID Parameters
Kp = 20
Kd = 12
Ki = 0
Ko = 50

# is the base in motion?
moving = 0

# PID setpoint info For a Motor
class SetPointInfo:
    TargetTicksPerFrame = 0.0   # target speed in ticks per frame
    Encoder = 0                 # encoder count
    PrevEnc = 0                 # last encoder count

    # Using previous input (PrevInput) instead of PrevError to avoid derivative kick,
    # see http://brettbeauregard.com/blog/2011/04/improving-the-beginner%E2%80%99s-pid-derivative-kick/
    PrevInput = 0               # last input
    PrevErr = 0                 # last error

    # Using integrated term (ITerm) instead of integrated error (Ierror),
    # to allow tuning changes,
    # see http://brettbeauregard.com/blog/2011/04/improving-the-beginner%E2%80%99s-pid-tuning-changes/
    ITerm = 0                   # integrated term
    output = 0                  # last motor setting
    def reset(self):
        self.TargetTicksPerFrame = 0.0
        self.Encoder = 0
        self.PrevEnc = self.Encoder
        self.PrevInput = 0  # last input
        self.PrevErr = 0  # last error
        self.ITerm = 0  # integrated term
        self.output = 0

left_PID = SetPointInfo()
right_PID = SetPointInfo()

def reset_PID():
    left_PID.reset()
    right_PID.reset()


def do_PID(p):
    input = p.Encoder - p.PrevEnc
    Perror = p.TargetTicksPerFrame - input

    # Avoid derivative kick and allow tuning changes,
    #  see http://brettbeauregard.com/blog/2011/04/improving-the-beginner%E2%80%99s-pid-derivative-kick/
    #  see http://brettbeauregard.com/blog/2011/04/improving-the-beginner%E2%80%99s-pid-tuning-changes/
    output = (Kp * Perror - Kd * (input - p.PrevInput) + p.ITerm) / Ko
    p.PrevEnc = p.Encoder

    output += p.output

    # Accumulate Integral error *or* Limit output.
    # Stop accumulating when output saturates
    if output >= MAX_PWM:
        output = MAX_PWM
    elif output <= -MAX_PWM:
        output = -MAX_PWM
    else:
        # allow turning changes, see http://brettbeauregard.com/blog/2011/04/improving-the-beginner%E2%80%99s-pid-tuning-changes/
        p.ITerm += Ki * Perror

    p.output = output
    p.PrevInput = input

# Read the encoder values and call the PID routine
def update_PID():
    # Read the encoders
    left_PID.Encoder = read_encoder(LEFT_ENCODER)
    right_PID.Encoder = read_encoder(RIGHT_ENCODER)

    # If we're not moving there is nothing more to do
    if moving != 0:
        # Reset PIDs once, to prevent startup spikes,
        # see http://brettbeauregard.com/blog/2011/04/improving-the-beginner%E2%80%99s-pid-initialization/
        # PrevInput is considered a good proxy to detect
        # whether reset has already happened
        if left_PID.PrevInput != 0 || right_PID.PrevInput != 0:
            reset_PID()
        return

    # Compute PID update for each motor
    do_PID(left_PID)
    do_PID(right_PID)

    # Set the motor speeds accordingly
    set_motor_speeds(left_PID.output, right_PID.output)