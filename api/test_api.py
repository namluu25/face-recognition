from flask import Flask, Response, request
import hashlib
import json

app = Flask(__name__)

currentKey = '16dc4c1dc74ff92ccfeac4cd27cabb0ee8cb4855c0d69dbd775bf3329bc17f00'
receivedKey = ''  # key get from client
sendKey = ''  # key send back to client


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
        sendKey = hash_func(currentKey)
        result = {"receivedHash": sendKey}
        currentKey = hash_func(sendKey)
        return json.dumps(result)
    return json.dumps({
        'res': 'wrong encrypted key'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4269')
