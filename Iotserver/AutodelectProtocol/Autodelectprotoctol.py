import struct 
import binascii
import time
import logging
import os
from comm.comm import loglocal
from twisted.python import log
from twisted.internet import defer

'''model_struct = {
	'model_name':'khb_product_1',
	'data_type' : {
				'A0':{'02':'Float','03':'Float'},
				'A1':{'03':'Float','04':'UInt'} 
	},
	'typemappointname': {
				'A0': {'02': 'current_1', '03': 'current_2', '04': 'Temp'}, 
				'A1': {'03': 'current_2', '04': 'Temp'}
	},
	'updata_procotol':....,
	....
}'''


#datastream = 'A11C0102030405060708090A0B0C0304bf9c28f604040000000A5D86'
#'A01C0102030405060708090A0B0C0204bf9c28f60304f6289c3f439A'

def AutoDelect(model_struct,datastream,sqlconnect):
	defer_intancs = defer.Deferred()
	UUID = datastream[4:36]
	typedict = model_struct['data_type'][datastream[0:2]]
	table_name = model_struct['model_name']+'_'+'Data'
	datapoint_set = datastream[36:-4]  #所有数据点集合
	onedatapoint_len = int(datapoint_set[2:4])*2+2+2# V + T + L
	nextdatapoint_len = 0
	field = ['UUID']
	datalist  = [UUID]
	try:
		for number in range(len(typedict)):
			value = typedict[datapoint_set[0+nextdatapoint_len:2+nextdatapoint_len]]
			field.append(model_struct['typemappointname'][datastream[0:2]][datapoint_set[0+nextdatapoint_len:2+nextdatapoint_len]])
			datalist.append(typetofunc[value](datapoint_set[0+nextdatapoint_len+2+2:onedatapoint_len+nextdatapoint_len]))
			nextdatapoint_len = nextdatapoint_len + onedatapoint_len
		defer_intancs.callback((save_data,table_name,field,datalist,sqlconnect))
	except Exception as e:
		defer_intancs.errback(e)
	return defer_intancs

def AutoDelectSuccess(argv):
	argv[2].append('Currenttime')
	argv[3].append(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	cur=argv[4].runInteraction(argv[0],argv[1],tuple(argv[2]),tuple(argv[3]))
	cur.addErrback(sql_error)

def AutoDelectFail(err):
	log.msg('AutoDelect error:{}'.format(err))

def delectchar(charstr):
	'''ASCII码'''
	s = struct.Struct('!c')
	return s.unpack(bytes.fromhex(charstr))[0]

def delectsingedchar(singedcharstr):
	'''有符号char整型数值'''
	s = struct.Struct('!b')
	return s.unpack(bytes.fromhex(singedcharstr))[0]	

def delectunsingedchar(unsingedcharstr):
	'''无符号char整型数值'''
	s = struct.Struct('!B')
	return s.unpack(bytes.fromhex(unsingedcharstr))[0]	

def delectbool(boolstr):
	'''bool型数值'''
	s = struct.Struct('!?')
	return s.unpack(bytes.fromhex(boolstr))[0]	

def delectshort(shortstr):
	'''有符号2个字节短整型'''
	s = struct.Struct('!h')
	return s.unpack(bytes.fromhex(shortstr))[0]

def delectunsingedshort(unsingedshortstr):
	'''无符号2个字节短整型'''
	s = struct.Struct('!H')
	return s.unpack(bytes.fromhex(unsingedshortstr))[0]

def delectint(intstr):
	'''有符号4个字节整型'''
	s = struct.Struct('!i')
	return s.unpack(bytes.fromhex(intstr))[0]	

def delectuint(uintstr):
	'''无符号4个字节整型'''
	s = struct.Struct('!I')
	return s.unpack(bytes.fromhex(uintstr))[0]

def delectlong(longstr):
	'''有符号4个字节整型'''
	s = struct.Struct('!l')
	return s.unpack(bytes.fromhex(longstr))[0]

def delectunsingedlong(unsingedlongstr):
	'''无符号4个字节整型'''
	s = struct.Struct('!L')
	return s.unpack(bytes.fromhex(unsingedlongstr))[0]

def delectlonglong(longlongstr):
	'''有符号8个字节整型'''
	s = struct.Struct('!q')
	return s.unpack(bytes.fromhex(longlongstr))[0]

def delectunsingedlonglong(unsingedlonglongstr):
	'''无符号8个字节整型'''
	s = struct.Struct('!Q')
	return s.unpack(bytes.fromhex(unsingedlonglongstr))[0]

def delectfloat(floatstr):
	'''有符号浮点型'''
	s = struct.Struct('!f')
	return round(s.unpack(bytes.fromhex(floatstr))[0],2)#round(f,2) 保留浮点型小数点后两位

def delectdouble(doublestr):
	'''有符号双精度浮点型'''
	s = struct.Struct('!d')
	return s.unpack(bytes.fromhex(doublestr))[0]	

def delecthexstr(hexstr):
	'''处理16进制字符串,适用于透传'''
	pass

def delectutf8str(utf8str):
	'''处理16进制字符串,适用于透传'''
	pass

def delectenum(enum):
	'''枚举'''
	pass

def delectasciistr(asciistr):
	'''acsiic 字符串'''
	pass

def delectbit(bit):
	'''位操作'''
	pass

def save_data(cursor,table_name,field,data):
	field = ','.join(field)
	sql_cmd= 'INSERT INTO {} ({}) VALUES {};'.format(table_name,field,data)
	#mylogger.info(sql_cmd)
	cursor.execute(sql_cmd)

def sql_error(err):
	log.msg('Insert error:{}'.format(err.getErrorMessage()))

typetofunc = {
	'Acsiibyte':delectchar,
	'Char'     :delectsingedchar,
	'UChar'    :delectunsingedchar,
	'Short'    :delectshort,
	'UShort'   :delectunsingedshort,
	'Int'      :delectint,
	'UInt'     :delectuint,
	'Long Long':delectunsingedlonglong,
	'ULong Long':delectunsingedlonglong,
	'Float'    :delectfloat,
	'Double'   :delectdouble,
	'Bool'     :delectbool,
	'Enum'     :delectenum,
	'HexStr'   :delecthexstr,
	'UTF8Str'  :delectutf8str,
	'AsciiStr' :delectasciistr,
	'Bit'      :delectbit
}

if __name__ == '__main__':

	'''typetofunc = {
		'Float':delectfloat,
		'UInt' :delectuint,
	}
	fd = -1.22
	s = struct.Struct('!f')
	f = s.pack(fd)
	print(f)
	fstr=binascii.hexlify(f).decode('utf-8')
	print(fstr)'''

	AutoDelect(model_struct,datastream)