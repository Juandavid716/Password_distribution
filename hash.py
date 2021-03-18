import sys
import hashlib

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

md5 = hashlib.md5()
sha1 = hashlib.sha1()

def get_hash(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

# def get_hash(name):
#     with open(name, 'rb') as f:
#         while True:
#             data = f.read(BUF_SIZE)
#             if not data:
#                 break
#             md5.update(data)
#             sha1.update(data)
#     print("xdd{0}".format(sha256sum(name)))
#     print("MD5: {0}".format(md5.hexdigest()))
#     # print("SHA1: {0}".format(sha1.hexdigest()))
#     return sha1.hexdigest()
    