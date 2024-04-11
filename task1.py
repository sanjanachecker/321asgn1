from ssl import RAND_bytes
import sys
from Crypto.Cipher import AES


# open file
image = sys.argv[1]
with open(image, 'rb') as image_file:
    im = image_file.read()

# get size of file
size = len(im)
print(f'File Size in Bytes is {size}')


def ecb(im, size):
    # need to ensure that file is evenly disible by 128-bits with PKCS#7 padding
    # then encrypt 128 bits at a time
    key = RAND_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)

    # pad file
    bytes_to_pad = size % 16
    pad_contents = hex(bytes_to_pad)
    padded_file = pad(im, bytes_to_pad, pad_contents)

    # print(padded_file)
    print('pad contents:', pad_contents)
    print('key = ', key)
    print(cipher)

    print(len(padded_file))
    # write to make encoded file
    for i in range(size/16):


def pad(im, numbytes, contents):
    # print('im', type(im))
    # print('cont', type(contents))
    # print('nb', type(numbytes))
    return im + (contents * numbytes).encode('utf-8')


def cbc(im):
    pass


ecb(im, size)
