import schedule
import threading
from flask import Flask, Response
import RPi.GPIO as GPIO
import time

pin = 17
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)

app = Flask(__name__)

def lock():
    GPIO.output(pin, GPIO.LOW)

def unlock():
    GPIO.output(pin,GPIO.HIGH)

def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

thread = threading.Thread(target=scheduler, name = 'Scheduler', daemon=True)
thread.start()

def lock_job():
    lock()
    return schedule.CancelJob

def schedule_lock():
    schedule.jobs.clear() #cancel all schedule jobs
    schedule.every(5).seconds.do(lock_job) #schedule lock job

@app.route('/unlock', methods=['GET'])
def unlock_route():
    unlock()
    schedule_lock()
    return Response(status=202)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=420)