import hashlib
import requests
import time


def send_request(key):
    url = 'http://10.0.50.125:4269/unlock'
    obj = {'currentHash': key}
    requests.post(url, data=obj)


def hash_func(x0):
    currentHash = x0
    temp = hashlib.sha256(currentHash.encode('utf-8'))
    futureHash = temp.hexdigest()

    hash_func(futureHash)
    return futureHash


key = 'D682ED4CA4D989C134EC94F1551E1EC580DD6D5A6ECDE9F3D35E6E4A717FBDE4'
# while True:
key = hash_func(key)
print(key)
# time.sleep(10)

# defaultHash ='D682ED4CA4D989C134EC94F1551E1EC580DD6D5A6ECDE9F3D35E6E4A717FBDE4'
# currentHash = ''
#
# m = hashlib.sha256(defaultHash.encode('utf-8'))
# currentHash = m.hexdigest()
#
# print(currentHash)
#
# url = 'http://10.0.50.125:4269/unlock'
# myobj = {'currentHash': currentHash}
#
# x = requests.post(url, data = myobj)
#
# print(x.status_code)
