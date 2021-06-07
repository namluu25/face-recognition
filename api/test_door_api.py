import schedule
import threading
from flask import Flask, Response, request
import hashlib
import json
import RPi.GPIO as GPIO
import time

pin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)

currentKey = '16dc4c1dc74ff92ccfeac4cd27cabb0ee8cb4855c0d69dbd775bf3329bc17f00'
receivedKey = ''  # key get from client
sendKey = ''  # key send back to client

app = Flask(__name__)


def lock():
    GPIO.output(pin, GPIO.LOW)


def unlock():
    GPIO.output(pin, GPIO.HIGH)


def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


thread = threading.Thread(target=scheduler, name='Scheduler', daemon=True)
thread.start()


def lock_job():
    lock()
    return schedule.CancelJob


def schedule_lock():
    schedule.jobs.clear()  # cancel all schedule jobs
    schedule.every(3).seconds.do(lock_job)  # schedule lock job


def hash_func(x0):
    currentKey = x0
    temp = hashlib.sha256(currentKey.encode('utf-8'))
    futureKey = temp.hexdigest()
    return futureKey

@app.route('/unlock', methods=['POST'])
def auth_check():
    global currentKey

    jsondata = request.get_json()
    data = json.loads(jsondata)
    receivedKey = data['currentHash']

    if receivedKey == currentKey:
        unlock()
        schedule_lock()
        sendKey = hash_func(currentKey)
        result = {"receivedHash": sendKey}
        currentKey = hash_func(sendKey)
        return json.dumps(result)
    return json.dumps({
        "receivedHash": "wrong encrypted key"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4269')
