def send_request():
	pass

def hash_func(x0):
	current_key = x0
	future_key 	= hash(x0)

	send_request() # send future_key to server

	return future_key

key = xx

# bat dau nhan dien khuon mat
while True:
	key = hash_func(key)