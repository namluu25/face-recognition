import math
# liveness check
def check_right(righteye, lefteye, nose, orig_eye_dist, orig_nose_x):
    dist = math.sqrt((righteye[0] - lefteye[0]) ** 2 + (righteye[1] - lefteye[1]) ** 2)
    if dist <= orig_eye_dist * 0.52 and nose[0] < orig_nose_x:
        return True
    else:
        return False


def check_left(righteye, lefteye, nose, orig_eye_dist, orig_nose_x):
    dist = math.sqrt((righteye[0] - lefteye[0]) ** 2 + (righteye[1] - lefteye[1]) ** 2)
    if dist <= orig_eye_dist * 0.52 and nose[0] > orig_nose_x:
        # tts.say("Turn to the left")
        return True
        # while True:

    else:
        return False
    # tts.runAndWait()