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


def ecb(im):
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


def cbc(im):
    pass


def main():
    # if len(sys.argv) < 4:
    print("Usage: ./run.sh input.bmp output_ecb.bmp output_cbc.bmp")
    # sys.exit(1)

    filename = sys.argv[1]
    output = sys.argv[2]
    # output_cbc = sys.argv[3]

    with open(filename, 'rb') as file:
        header = file.read(54)  # or 138 if not working
        image = file.read()

    encrypted_im_ecb, key_ecb = ecb(image)
    with open(output, 'wb') as output_file:
        output_file.write(header)
        output_file.write(encrypted_im_ecb)

    print("ECB encryption key:", key_ecb)


if __name__ == "__main__":
    main()
