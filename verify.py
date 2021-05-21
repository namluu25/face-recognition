import time
import pyttsx3

from src.embedding import create_embeddings
from src.recognition import recognize_engine

# add text-to-speech
tts = pyttsx3.init()

input_embeddings = create_embeddings()

time.sleep(1)

while True:
    if input_embeddings != {}:
        print("Face Verification in process")
        # tts.runAndWait()
        recognize_engine(input_embeddings)
    else:
        print("No User Found")

    time.sleep(5)
