import time
import pyttsx3

from src.embeeding import create_input_image_embeddings
from src.recognition import recognize_faces_in_cam_50

# add text-to-speech
tts = pyttsx3.init()

while True:
    input_embeddings = create_input_image_embeddings()
    if input_embeddings != {}:
        print("Face Verification in process")
        # tts.runAndWait()
        recognize_faces_in_cam_50(input_embeddings)
    else:
        print("No User Found")

    time.sleep(5)
