from task1 import cbc, ecb
from ssl import RAND_bytes

def pad(data, block_size=16):
    padding_len = block_size - len(data) % block_size
    padding = bytes([padding_len] * padding_len)
    return data + padding
    
def submit(user_string):
    key = RAND_bytes(16)
    iv = RAND_bytes(16)

    # URL encode ; and = in the user string 
    encoded_string = user_string.replace(";", "%3B")
    encoded_string = encoded_string.replace("=", "%3D")

    # prepend and append given strings
    encoded_plaintext = f"userid=456;userdata={encoded_string};session-id=31337".encode() # encodes by utf8
    print(encoded_plaintext)
    encoded_plaintext = pad(encoded_plaintext)

    # use cbc to encode
    ciphertext, key, iv = cbc(encoded_plaintext)
    return ciphertext

def verify():
    pass

print(submit("hello"))
