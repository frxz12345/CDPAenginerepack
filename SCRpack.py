import os, struct

arc = 'SCR'
newarc = 'CN_'
def from_bytes(a: bytes):
    return int.from_bytes(a, byteorder='little')

def 解包(p1):
    f = open(arc, 'rb')
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
        data = fl[filepos:filepos + filesize]
        for b in data:
            b = b^0x80
            f1.write(struct.pack('B',b))
        f1.close()
    f.close()


p1 = './temp\\'
p2 = './cn\\'
if not os.path.exists(p1):
    os.mkdir(p1)
if not os.path.exists(p2):
    os.mkdir(p2)
解包(p1)
# exit(1)
files = os.listdir(p2)
fw = open(newarc, 'wb')
l1 = len(files) * [0]
i = 0
fw.write(b'\x50\x41\x43\x4B')
filecont = len(files)
fw.write(struct.pack('i', filecont))
filestart = len(files) * 40 + 8
pos = filestart
for file in files:
    fl = (32 - len(file))
    filename = file.encode('cp932') + b'\x00' * fl
    filesize = os.stat(p2 + file).st_size
    filepos = pos
    pos = pos + filesize
    fw.write(filename)
    fw.write(struct.pack('i', filesize))
    fw.write(struct.pack('i', filepos))
for file in files:
    f = open(p2 + file, 'rb')
    data = f.read()
    for b in data:
        b = b ^ 0x80
        fw.write(struct.pack('B', b))
    f.close()
fw.close()
