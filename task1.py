import sys
from PIL import Image
from Crypto.Cipher import AES

# open file
image = sys.argv[1]
im = Image.open(image)
im.show()


def ecb(im):
    # need to ensure that file is evenly disible by 128-bits with PKCS#7 padding
    # then encrypt 128 bits at a time
    # key =
    cipher = AES.new(key, AES.MODE_ECB)


def cbc(im):
    pass
