
LEFT_ENCODER = 0
RIGHT_ENCODER = 1

LEFT_ENC_PIN_A = 2
LEFT_ENC_PIN_B = 3
RIGHT_ENC_PIN_A = 4
RIGHT_ENC_PIN_B = 5

left_enc_pos = 0
right_enc_pos = 0
ENC_STATES = {0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0}

# Interrupt routine for LEFT encoder, taking care of actual counting
def ISL: # interrupt !!!!
    enc_last = 0
    enc_last <<= 2 # shift previous state two places
    enc_last |= (PIND & (3 << 2)) >> 2 # read the current state into lowest 2 bits
    left_enc_pos += ENC_STATES[(enc_last & 0x0f)]

# Interrupt routine for RIGHT encoder, taking care of actual counting
def ISR:
    enc_last = 0
    enc_last <<= 2 # shift previous state two places
    enc_last |= (PIND & (3 << 2)) >> 2 # read the current state into lowest 2 bits
    right_enc_pos += ENC_STATES[(enc_last & 0x0f)]


def read_encoder(i):
    if i == LEFT_ENCODER:
        return left_enc_pos
    else:
        return right_enc_pos

def reset_encoder(i):
    if i == LEFT_ENCODER:
        left_enc_pos = 0
        return
    else:
        right_enc_pos = 0
        return
def reset_encoders():
    reset_encoder(LEFT_ENCODER)
    reset_encoder(RIGHT_ENCODER)