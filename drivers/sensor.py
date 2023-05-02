# Encoder logic

# The speed of sound is 340 m/s or 29 microseconds per cm.
# The ping travels out and back, so to find the distance of the
# object we take half of the distance travelled.
def microseconds_to_cm(microseconds) :
    return microseconds / 29 / 2
