from task1 import cbc, ecb

def submit(user_string, key, iv):

    # URL encode ; and = in the user string 
    encoded_string = user_string.replace(";", "%3B")
    encoded_string = encoded_string.replace("=", "%3D")

    # prepend and append given strings
    encoded_plaintext = f"userid=456;userdata={encoded_string};session-id=31337".encode()
    encoded_plaintext = pad(encoded_plaintext)

    ciphertext, key, iv = cbc(encoded_plaintext)
    return ciphertext

def verify():
    pass