''' 全局变量 '''
import time

#数据类型对照表
mysqldatabasename = 'django'

data_type_list = {
	'number':{
		'Char(-2^7-1 ~ 2^7,1字节)':'Char',	
		'uChar(0 ~ 2^8,1字节)'	:'UChar',											
		'Short(-2^15-1 ~ 2^15,2字节)':'Short',
	    'uShort(0 ~ 2^16,2字节)' :'UShort',                                        				
	    'Int(-2^31-1~ 2^31,4字节)':'Int' ,                                       
	    'uInt(0 ~ 2^32,4字节)'  :'UInt'  ,                                       
		'Long Long(-2^63-1 ~ 2^63,8字节)':'Long Long',											
	    'uLong Long(0 ~ 2^64,8字节)':'ULong Long',                                          
		'Float(-3.40282^-38 ~ 3.40282^38,4字节)':'Float',											
		'Double(-1.79769^-308 ~ 1.79769^308,8字节)':'Double',
	},											
	'Bool(布尔,单字节)':'Bool',											
	'Enum(枚举,单字节)':'Enum',											
	'String(十六进制)':'HexStr',											
	'String(UTF-8编码)'	:'UTF8Str',
	'String(ASCII码)':'AsciiStr'									
}

def TypeConvert(data_type):
	for Types,values in data_type_list.items():
		if data_type == Types:
			return values
		else:
			try:
				for Type,value in values.items():
					if data_type == Type:
						return value
			except AttributeError:
				continue

if __name__ == '__main__':
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
	print(TypeConvert( 'Bool(布尔，单字节)'))
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))