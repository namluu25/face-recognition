import hashlib
import json
import requests

url = 'http://192.168.0.193:4269/unlock'
currentHash = '6dc1ea4fabedfd580bf32d4614f4170db3d86bc3656f8fce25f39a4f81eec1bc'
sendHash = ''
receivedHash = ''


def hash_func(key):
    current = key
    temp = hashlib.sha256(current.encode('utf-8'))
    futureHash = temp.hexdigest()
    return futureHash


def send_key():
    global currentHash, sendHash, receivedHash
    sendHash = hash_func(currentHash)

    data = {'currentHash': sendHash}
    s = json.dumps(data)

    res = requests.post(url, json=s).json()
    currentHash = res['receivedHash']
