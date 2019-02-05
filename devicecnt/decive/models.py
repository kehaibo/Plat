from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import connection
 
# Create your models here.
class ProductModelName(models.Model):
	''' 模型名字及简单描述'''
	product_model = models.CharField(max_length=64,unique=True)
	product_desc  = models.CharField(blank=True,max_length=64)
	current_time  = models.DateTimeField(auto_now=True,blank=True)
	create_time   = models.DateTimeField(auto_now=True,blank=True)
	user          = models.ForeignKey(get_user_model(),to_field='username')
	protocol_type = models.CharField(max_length=64,default="")

class data_point(models.Model):
	''' 数据体中的数据点'''
	model_name = models.ForeignKey(ProductModelName,default='')
	#attr       = models.ForeignKey(stream_point_attr,default='')
	data_name = models.CharField(max_length=64)
	show_name = models.CharField(max_length=64)
	TLV_Type  = models.CharField(max_length=4,default='')
	operation_type = models.CharField(max_length=2)#t只读/读写
	data_type = models.CharField(max_length=12) #数据类型

	#整型上限及下限、步进值表单内容
	max_value = models.CharField(max_length=64,blank=True) #最大值
	min_value = models.CharField(max_length=64,blank=True) #最小值
	step_by_step = models.CharField(max_length=64,blank=True) #步进值
	value_unit = models.CharField(max_length=12) #数据单位

	#bool型值名称，及显示名称表单内容
	true_value_name = models.CharField(max_length=64,blank=True)
	true_value_show = models.CharField(max_length=64,blank=True)
	true_bool_value = models.NullBooleanField(null=True,blank=True)
	false_value_name = models.CharField(max_length=64,blank=True)
	false_value_show = models.CharField(max_length=64,blank=True)
	false_bool_value = models.NullBooleanField(blank=True)

	#字符串数据长度表单
	str_maxlen = models.CharField(max_length=64,blank=True)

	def __str__(self):
		return self.show_name

class upstream(models.Model):
	''' 上行数据体'''
	model_name      = models.ForeignKey(ProductModelName,default='')#关联模型名字
	#point           = models.ForeignKey(data_point,default='')
	stream_showname = models.CharField(max_length=64,default='')
	stream_name     = models.CharField(max_length=64,default='')
	stream_Type     = models.CharField(max_length=4,default='')
	stream_len      = models.CharField(max_length=4,default='')
#	point_attr      = models.CharField(max_length=1,default='')#1:下行;2:上行;3:下行响应;4:上行响应
	#upordown        = models.CharField(max_length=1,default='')

class downstream(models.Model):
	'''下行数据体'''
	model_name      = models.ForeignKey(ProductModelName,default='')#关联模型名字
	#point           = models.ForeignKey(data_point,default='')
	stream_showname = models.CharField(max_length=64,default='')
	stream_name     = models.CharField(max_length=64,default='')
	stream_Type     = models.CharField(max_length=4,default='')
	stream_len      = models.CharField(max_length=4,default='')
	#point_attr      = models.CharField(max_length=1,default='')#1:下行;2:上行;3:下行响应;4:上行响应

class upstream_datapoint(models.Model):
	'''上行数据与数据点的关联(多对多)'''
	model_name    = models.ForeignKey(ProductModelName,default='')#关联模型名字
	upstream      = models.ForeignKey(upstream,default='')
	data_point    = models.ForeignKey(data_point,default='')
	point_attr    = models.CharField(max_length=1,default='')#1:下行;2:上行;3:下行响应;4:上行响应

class downstream_datapoint(models.Model):
	'''下行数据与数据点的关联'''
	model_name    = models.ForeignKey(ProductModelName,default='')#关联模型名字
	downstream    = models.ForeignKey(downstream,default='')
	data_point    = models.ForeignKey(data_point,default='')
	point_attr    = models.CharField(max_length=1,default='')#1:下行;2:上行;3:下行响应;4:上行响应

class Deviceinfo(models.Model):
	'''设备信息'''
	device_user = models.ForeignKey(get_user_model(),to_field='username')#关联用户
	model_name = models.ForeignKey(ProductModelName,default='')
	UUID = models.CharField(max_length=32,blank=True)
	device_name = models.CharField(max_length=64,blank=True)#设备名称
	device_class = models.CharField(max_length=64,blank=True)#设备行业类型
	device_desc  = models.CharField(max_length=100,default='')#设备描述
	#device_status = models.ForeignKey(DeviceStatus,default='')
	create_time = models.DateTimeField(auto_now=True,blank=True)

class DeviceStatus(models.Model):
	'''设备状态'''
	device = models.ForeignKey(Deviceinfo,default='')#关联设备信息，用于前端展示设备状态
	UUID = models.CharField(max_length=32,blank=True)
	status = models.CharField(max_length=1,blank=True)
	info = models.CharField(max_length=10,blank=True)
	currenttime =  models.DateTimeField(auto_now=True,blank=True)
		
class AddDeciveDataTable():
	'''添加设备日记表'''
	def __init__(self,table_name):
		self.table_name = str(table_name)+'_'+'Data'

	def create_table(self):
		'''创建数据表'''
		sql_cmd = 'CREATE TABLE IF NOT EXISTS {} ( id int(11) NOT NULL AUTO_INCREMENT,UUID varchar(32) NOT NULL,Currenttime datetime NOT NULL,PRIMARY KEY (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;'.format(self.table_name)
		cur = connection.cursor()
		cur.execute(sql_cmd)
		cur.close()

	def remove_table(self):
		'''删除数据表'''
		sql_cmd = 'DROP TABLE {};'.format(self.table_name)
		cur = connection.cursor()
		cur.execute(sql_cmd)
		cur.close()

	def add_field(self,field):
		'''添加数据表字段'''
		sql_cmd = 'alter table {}  add {} varchar(32)  Null;'.format(self.table_name,field)
		cur = connection.cursor()
		cur.execute(sql_cmd)
		cur.close()

	def remove_field(self,field):
		'''删除数据表字段'''
		sql_cmd = 'alter table {} drop column {};'.format(self.table_name,field)
		cur = connection.cursor()
		cur.execute(sql_cmd)
		cur.close()



