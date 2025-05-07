import os, struct


def from_bytes(a: bytes):
    return int.from_bytes(a, byteorder='little')


def 解包(p1):
    f = open('bg', 'rb')
    fl = f.read()
    x = fl[4:8]
    filescont = from_bytes(x)
    for i in range(filescont):
        x = 8 + i * 40
        y = 8 + i * 40 + 40
        z = fl[x + 32:y - 4]
        filename = fl[x:y - 8].decode('CP932').replace('\x00', '')
        filesize = from_bytes(z)
        z = fl[x + 36:y]
        filepos = from_bytes(z)
        print(filename)
        print(hex(filesize))
        print(hex(filepos))
        f1 = open(p1 + filename, 'wb')
        f1.write(fl[filepos:filepos + filesize])
        f1.close()
    f.close()


p1 = './temp\\'
p2 = './pnj\\'
if not os.path.exists(p1):
    os.mkdir(p1)
for i in os.listdir(p2):
    fp = open(p2 + i, 'rb')
    bp = fp.read()
    fp.close()
    fp = open(p1 + i, 'wb')
    fp.write(bp)
    fp.close()
解包(p1)
# exit(1)
files = os.listdir(p1)
fw = open('BB', 'wb')
l1 = len(files) * [0]
i = 0
fw.write(b'\x50\x41\x43\x4B')  ##BG
filecont = len(files)
fw.write(struct.pack('i', filecont))
'''
95 02 -> 16 03
'''
filestart = len(files) * 40 + 8
pos = filestart
for file in files:  # 9680
    fl = (32 - len(file))
    filename = file.encode('cp932') + b'\x00' * fl
    filesize = os.stat(p1 + file).st_size
    filepos = pos
    pos = pos + filesize
    fw.write(filename)
    fw.write(struct.pack('i', filesize))
    fw.write(struct.pack('i', filepos))
for file in files:
    f = open(p1 + file, 'rb')
    fw.write(f.read())
    f.close()
fw.close()
files = os.listdir(p1)
for i in files:
    os.remove(p1 + i)
