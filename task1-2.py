from ssl import RAND_bytes
import sys
from Crypto.Cipher import AES

def pad(data, block_size=16):
    padding_len = block_size - len(data) % block_size
    padding = bytes([padding_len] * padding_len)
    return data + padding


def unpad(data, block_size=16):
    # print("data to unpad:", data)
    # print("last byte:",data[-1])
    padding_len = data[-1]
    return data[:-padding_len]

def ecb_encrypt(im):
    # need to ensure that file is evenly disible by 128-bits with PKCS#7 padding
    # then encrypt 128 bits at a time
    key = RAND_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)

    # pad file
    padded_file = pad(im)

    # print(padded_file)
    print('key = ', key)
    print(cipher)

    print(len(padded_file))
    # write to make encoded file
    encrypted_data = b''
    for i in range(0, len(padded_file), 16):
        block = padded_file[i:i+16]
        encrypted_data += cipher.encrypt(block)

    return encrypted_data, key


def cbc_encrypt(im):
    key = RAND_bytes(16)
    iv = RAND_bytes(16)

    cipher = AES.new(key, AES.MODE_ECB)
    padded_file = pad(im)

    encrypted_data = bytes()
    prev_block = iv

    for i in range(0, len(padded_file), 16):
        block = padded_file[i:i+16]
        # xor with previous block before encrypting
        block = bytes(x ^ y for x, y in zip(block, prev_block))
        encrypted_block = cipher.encrypt(block)
        encrypted_data += encrypted_block
        prev_block = encrypted_block

    return encrypted_data, key, iv


def cbc_decrypt(encrypted_string, key, iv):

    cipher = AES.new(key, AES.MODE_ECB)

    decrypted_data = b''
    prev_block = iv

    for i in range(0, len(encrypted_string), 16):
        encrypted_block = encrypted_string[i:i+16]
        decrypted_block = cipher.decrypt(encrypted_block)
        # xor with previous block after decrypting
        decrypted_block = bytes(
            x ^ y for x, y in zip(decrypted_block, prev_block))
        decrypted_data += decrypted_block
        prev_block = encrypted_block

    decrypted_data = unpad(decrypted_data)
    # print("decrypted data:", decrypted_data)

    return decrypted_data

def submit(user_string):
    # URL encode ; and = in the user string 
    encoded_string = user_string.replace(";", "%3B")
    encoded_string = encoded_string.replace("=", "%3D")

    # prepend and append given strings
    encoded_plaintext = f"userid=456;userdata={encoded_string};session-id=31337".encode() # encodes by utf8
    # print("enccoded plaintext", encoded_plaintext)
    encoded_plaintext = pad(encoded_plaintext)

    # use cbc to encode
    ciphertext, key, iv = cbc_encrypt(encoded_plaintext)
    # print("ciphertext:", ciphertext)
    return ciphertext, key, iv


def verify(encrypted_string, key, iv):
    # decrypt string w cbc 
    # parse string for pattern ;admin=true
    # return true if ";admin=true" exists, false otherwise
    # note: should be impossible for user to provide input to submit() that will make verify() return true
    decrypted_data = cbc_decrypt(encrypted_string, key, iv)
    print("decrypted data:",decrypted_data)
    admin_encoded = ";admin=true;".encode()
    return admin_encoded in decrypted_data

def bit_flip(ciphertext):
    ciphertext_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    target_block = ciphertext_blocks[0] # we want to modify first block because when chained, will xor with second block
    xor1 = ord('4') ^ ord(';') # what to xor with to get ;
    xor2 = ord('5') ^ ord('=') # what to xor with to get = 
    mod_cipher_block = target_block[:4] + bytes([target_block[4] ^ xor1]) + target_block[5:10] + bytes([target_block[10] ^ xor2]) + target_block[11:15] + bytes([target_block[15] ^ xor1])
    print("modified cipher block:", mod_cipher_block)
    ciphertext_blocks[0] = bytes(mod_cipher_block)
    modified_ciphertext = b''.join(ciphertext_blocks)
    return modified_ciphertext

def main():
    # # if len(sys.argv) < 4:
    # print("Usage: ./run.sh input.bmp output_ecb.bmp output_cbc.bmp")
    # # sys.exit(1)

    # filename = sys.argv[1]
    # output_ebc = sys.argv[2]
    # output_cbc = sys.argv[3]
    # output_cbc_decrypt = sys.argv[4]

    # # ebc encrypt
    # with open(filename, 'rb') as file:
    #     header = file.read(54)  # or 138 if not working
    #     image = file.read()

    # encrypted_im_ecb, key_ecb = ecb_encrypt(image)
    # with open(output_ebc, 'wb') as output_file:
    #     output_file.write(header)
    #     output_file.write(encrypted_im_ecb)

    # print("ECB encryption key:", key_ecb)

    # # cbc encrypt
    # encrypted_im_cbc, key, iv = cbc_encrypt(image)
    # with open(output_cbc, 'wb') as output_file:
    #     output_file.write(header)
    #     output_file.write(encrypted_im_cbc)

    # print("CBC encyption key:", key, "IV:", iv)

    # # cbc decrypt
    # decrypted_data = cbc_decrypt(encrypted_im_cbc, key, iv)
    # with open(output_cbc_decrypt, 'wb') as output_file:
    #     output_file.write(header)
    #     output_file.write(decrypted_data)
    
    # # submit
    # submit_ciphertext, web_key, web_iv = submit("hello")
    # print(submit_ciphertext)


    user_attack = "4admin5true4"
    cipher, key, iv = submit(user_attack)
    print("cipher:",cipher)
    mod_cipher = bit_flip(cipher)
    print("decrypted data without modifying:", cbc_decrypt(cipher, key, iv))
    print("modified cipher:", mod_cipher)
    val = verify(mod_cipher, key, iv)
    print(val)


if __name__ == "__main__":
    main()
