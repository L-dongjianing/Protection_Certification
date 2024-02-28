import base64
import json

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import random


def getRandomSet(bits):
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    total_set = num_set + char_set

    value_set = "".join(random.sample(total_set, bits))

    return value_set


class PrpCrypt(object):
    def __init__(self, iv):
        self.key = "hexikejijiushinb".encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = iv

    def pad_byte(self, b):
        bytes_num_to_pad = AES.block_size - (len(b) % AES.block_size)

        byte_to_pad = bytes([bytes_num_to_pad])
        padding = byte_to_pad * bytes_num_to_pad
        padded = b + padding
        return padded

    def encrypt(self, text):
        self.iv, datee = text[0:16].encode("utf-8"), text[16:].encode('utf-8')
        cryptor = AES.new(self.key, self.mode, self.iv)
        text = self.pad_byte(datee)
        self.ciphertext = cryptor.encrypt(text)
        cryptbase64 = str(self.iv.decode('utf-8')) + str(base64.b64encode((self.ciphertext)).decode('utf8'))
        return cryptbase64

    def decrypt(self, text1):
        iv, text = text1[0:16].encode('utf-8'), str(text1[16:])
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        base64Str = base64.b64decode(text.encode('utf8'))
        cryptor = AES.new(self.key, self.mode, iv)
        aesStr = cryptor.decrypt(a2b_hex(base64Str))
        aesStr = str(unpad(aesStr), encoding='utf8')

        return aesStr


# if __name__ == '__main__':
# mfevhpq3s8e8qyxxQUQzN0Y0MEVBNDE0MTM1QjdDMzQ3M0RBRkY0NjNEQUM=
# data = {'password':123456,'uname':'djnnn','presentIP':'127.0.0.1'}  # '''被加密的内容'''
iv = getRandomSet(16)  # 16位每次随机的iv偏移
# print("偏移量是：", iv)
pc = PrpCrypt(str(iv))  # '''声明这个'''

# a = pc.decrypt('w4oaq66yju740e74QTJERDBFMTRDMkY0RDgwNDJDQ0Q1MTBGQ0IzNkIxRUM1OUNCMjRCQjkyMjcxNzIwNUNCN0QzMUNEMURCREM2REM2RUNBNTFEOTEwRkJCRkQ2RTI3NzkyREUxQ0E1RTBFMzNGQ0E1QzM5RDAyOTAxQjY4RDE1ODk4MTdBNTQ4MjNGMjZEMkQzRDk3NTM2RTczOUQ0NUE0MDUwNEI0NzExOUU5RTJDNTk4Mzg3MjQ1NTIxM0UwQjE2NTI5OTg1QzRGMEM4OUIzNDQ2M0M0RjhDMDQ1NjE4QjE4NDREQ0NCNjI=')

# print(pc.encrypt(pc.iv + str(data)))
# a = pc.decrypt('lc02kgmte39irznxcexqyGNRYsCdG+A3CjPsx4VxRvY0E/oq5kvAteDczyhuh/j/+N4qh+VdQMGqnnXqBNnGyH3ut/UDvedNxhOJX7XerG28XxyYd6yFoFC+f/E=')
# lis = pc.encrypt(lis)
# print(a)
# print(iv)
# print(lis)