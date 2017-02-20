import StringIO
from Crypto.Cipher import AES
import binascii
import base64

def add_padding_pkcs7(s):
    l = len(s)
    output = StringIO.StringIO()
    val = 16 - (l % 16)
    for _ in xrange(val):
        output.write('%02x' % val)
    return s + binascii.unhexlify(output.getvalue())

def del_padding_pkcs7(s):
    nl = len(s)
    val = int(binascii.hexlify(s[-1]), 16)
    if val > 16:
        raise ValueError('Input is not padded or padding is corrupt')

    l = nl - val
    return s[:l]

def encryptByKey(key, orgtext, iv):
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    result = encryptor.encrypt(add_padding_pkcs7(orgtext))
    return base64.b64encode(result)


def decryptByKey(key, orgtext, iv):
    orgtext = orgtext.replace(' ', '+')
    orgtext = base64.b64decode(orgtext)
    decryptor = AES.new(key, AES.MODE_CBC, iv)
    result = decryptor.decrypt(orgtext)
    return del_padding_pkcs7(result)


if __name__ == "__main__":
    iv = "78afc8512559b62f"
    orgtext = "c6d1965bf800d5f7682636826c9a097e"
    encrypted = encryptByKey(iv, orgtext, iv)

    print '#####encrypted: ', encrypted
    print '#####decrypted: ', decryptByKey(iv, encrypted, iv)
