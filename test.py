import requests
import time

while True:
    url = 'http://10.0.50.125:4269/unlock'
    myobj = {'payload': '1'}

    x = requests.post(url, data = myobj)

    print(x.status_code)

    time.sleep(5)