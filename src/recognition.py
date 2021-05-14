import imutils
from imutils.video import VideoStream
import math
import random
import cv2
from mtcnn import MTCNN

from src.liveness import check_left, check_right
from src.attendance import Attendance
from src.embeeding import recognize_face, model

detector = MTCNN()
face_cascade = cv2.CascadeClassifier('./model/haarcascade_frontalface_alt.xml')
# Function for Real Time Tests
def real_time_tests(name):
    tasks = ['Right', 'Left']
    tasks = random.sample(tasks, 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    count, tasks_completed, out = 0, 0, 0
    status = False
    # cam = cv2.VideoCapture(0)
    cam = VideoStream(src=0).start()

    while True:
        # image extraction from android phone camera using IP Webcam
        image = cam.read()
        image = imutils.resize(image, width=320)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = detector.detect_faces(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if len(result) != 0:
            bounding_box = result[0]['box']
            keypoints = result[0]['keypoints']
            cv2.rectangle(image, (bounding_box[0], bounding_box[1]),
                          (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]), (0, 155, 255), 2)
            cv2.circle(image, (keypoints['left_eye']), 2, (0, 155, 255), 2)
            cv2.circle(image, (keypoints['right_eye']), 2, (0, 155, 255), 2)
            cv2.circle(image, (keypoints['nose']), 2, (0, 155, 255), 2)
            cv2.circle(image, (keypoints['mouth_left']), 2, (0, 155, 255), 2)
            cv2.circle(image, (keypoints['mouth_right']), 2, (0, 155, 255), 2)

            # Storing Defaults
            if count == 0:
                original_eye_dist = math.sqrt((keypoints['right_eye'][0] - keypoints['left_eye'][0]) ** 2 + (
                            keypoints['right_eye'][1] - keypoints['left_eye'][1]) ** 2)
                # print("Original Eye Distance = ",original_eye_dist)
                original_mouth_dist = math.sqrt((keypoints['mouth_right'][0] - keypoints['mouth_left'][0]) ** 2 + (
                            keypoints['mouth_right'][1] - keypoints['mouth_left'][1]) ** 2)
                # print("Original Lip Distance = ",original_mouth_dist)
                original_nose_x = keypoints['nose'][0]
                count += 1
                continue

            task = tasks[0]
            image = cv2.resize(image, (800, 800))
            image = cv2.putText(image, task, (350, 25), font, 0.75, (255, 255, 255), 2)
            cv2.imshow("Test", image)
            if task == 'Right':
                status = check_right(keypoints['right_eye'], keypoints['left_eye'], keypoints['nose'],
                                     original_eye_dist, original_nose_x)

            elif task == 'Left':
                status = check_left(keypoints['right_eye'], keypoints['left_eye'], keypoints['nose'],
                                    original_eye_dist, original_nose_x)

            if status:
                tasks_completed += 1
                tasks = tasks[1:]
            count += 1
        else:
            out += 1
            continue
        if cv2.waitKey(1) == 27 or tasks_completed == 2 or out > 1:
            break

    cam.stop()
    cv2.destroyAllWindows()

    if tasks_completed == 2:
        # tts.say
            print("Welcome " + name)
    else:
        # tts.say
            print("Access Denied")
    # tts.runAndWait()

def recognize_faces_in_cam_50(input_embeddings):
    count = 0
    confirmation = 0
    name = ''

    # cam = cv2.VideoCapture(0)
    cam = VideoStream(src=0).start()
    while count <= 5 and confirmation < 2:
        frame = cam.read()
        frame = imutils.resize(frame, width=320)
        img = frame
        height, width, channels = frame.shape

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Loop through all the faces detected
        identities = ''
        if len(faces) != 0:
            for (x, y, w, h) in faces:
                x1 = x
                y1 = y
                x2 = x + w
                y2 = y + h

                face_image = frame[max(0, y1):min(height, y2), max(0, x1):min(width, x2)]
                identity = recognize_face(face_image, input_embeddings, model)

                if identity is not None:
                    confirmation += 1
                    name = identity
                    Attendance(name)
            count += 1
        else:
        #     tts.say("Please be infront of the camera")
        # tts.runAndWait()
            print("Please be infront of the camera")
    cam.stop()
    cv2.destroyAllWindows()

    if confirmation == 2:
        print("Face Verification done")
        print("Testing.")
        real_time_tests(name)
    else:
    #     tts.say("Access Denied")
    # tts.runAndWait()
        print("Access Denied")