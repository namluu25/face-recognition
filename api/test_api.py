from flask import Flask, Response, request
import hashlib

app = Flask(__name__)

currentKey = '574146c354c05d5705be0f8d0177187e1dbeb5c9e5be9863566df53e948508f4'
receivedKey = ''
sendKey = ''

def hash_func(x0):
    currentHash = x0
    temp = hashlib.sha256(currentHash.encode('utf-8'))
    futureHash = temp.hexdigest()
    return futureHash

@app.route('/unlock', methods=['POST', 'GET'])

def auth_check():
    global currentKey
    key = request.form.get("currentHash")
    print(key)
    receivedKey = key
    print(receivedKey)
    if receivedKey == currentKey:
        sendKey = hash_func(currentKey)
        print(sendKey)
        currentKey = hash_func(sendKey)
        return Response(status=200, data= {"receivedHash": sendKey})
    else:
        return Response(status=403)

@app.route('/test', methods=['GET'])

def test():
    abc = hash_func(currentKey)
    print(abc)
    return Response(status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4269')