import cv2

def store_sample(name):
    face_detector = cv2.CascadeClassifier('./model/haarcascade_frontalface_alt.xml')
    count = 0

    cam = cv2.VideoCapture(0)
    while (True):
        _, img = cam.read()

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(img, 1.3, 5)
        for (x, y, w, h) in faces:
            x1 = x
            y1 = y
            x2 = x + w
            y2 = y + h
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            count += 1
            # Save the captured image into the datasets folder
            if count == 5:
                cv2.imwrite("./data/datasets/" + name + ".jpg", img[y1:y2, x1:x2])
            cv2.imshow('image', img)

        if cv2.waitKey(1) == 27 or count >= 5:
            break
    cam.release()
    cv2.destroyAllWindows()


name = input("Enter your Name and be ready infront of camera: ")
store_sample(name)
print("Registration Successful")
