from ssl import RAND_bytes
import sys
from Crypto.Cipher import AES


# # open file
# image = sys.argv[1]
# with open(image, 'rb') as image_file:
#     im = image_file.read()

# # get size of file
# size = len(im)
# print(f'File Size in Bytes is {size}')


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


def pad(data, block_size=16):
    padding_len = block_size - len(data) % block_size
    padding = bytes([padding_len] * padding_len)
    return data + padding


def unpad(data, block_size=16):
    padding_len = data[-1]
    return data[:-padding_len]


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

    return decrypted_data


def main():
    # if len(sys.argv) < 4:
    print("Usage: ./run.sh input.bmp output_ecb.bmp output_cbc.bmp")
    # sys.exit(1)

    filename = sys.argv[1]
    output_ebc = sys.argv[2]
    output_cbc = sys.argv[3]
    output_cbc_decrypt = sys.argv[4]

    # ebc
    with open(filename, 'rb') as file:
        header = file.read(54)  # or 138 if not working
        image = file.read()

    encrypted_im_ecb, key_ecb = ecb_encrypt(image)
    with open(output_ebc, 'wb') as output_file:
        output_file.write(header)
        output_file.write(encrypted_im_ecb)

    print("ECB encryption key:", key_ecb)

    # cbc encrypt
    encrypted_im_cbc, key, iv = cbc_encrypt(image)
    with open(output_cbc, 'wb') as output_file:
        output_file.write(header)
        output_file.write(encrypted_im_cbc)

    print("CBC encyption key:", key, "IV:", iv)

    # cbc decrypt
    decrypted_data = cbc_decrypt(encrypted_im_cbc, key, iv)
    with open(output_cbc_decrypt, 'wb') as output_file:
        output_file.write(header)
        output_file.write(decrypted_data)


if __name__ == "__main__":
    main()
