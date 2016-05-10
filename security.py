import hmac

SECRET = "ww-padminsareassholes"

def hash_function(str):
	return hmac.new(str, SECRET).hexdigest()