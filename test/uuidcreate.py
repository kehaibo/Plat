import uuid
import time,hashlib



for i in range(1):
	print(uuid.uuid1())#生成唯一ID方法一

#第二种方法：
md5obj = hashlib.md5(str(time.clock()).encode('utf-8'))
ID = md5obj.hexdigest()
print(ID)
idhex =bytes.fromhex(ID)
print(idhex)
ID = idhex.hex()
print(ID)

