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
	user = models.ForeignKey(get_user_model(),to_field='username')

class stream(models.Model):
	''' 数据体'''
	model_name      = models.ForeignKey(ProductModelName,default='')#关联模型名字
	point           = models.ManyToManyField('data_point')
	stream_showname = models.CharField(max_length=64,default='')
	stream_name     = models.CharField(max_length=64,default='')
	stream_Type     = models.CharField(max_length=4,default='')
	stream_len      = models.CharField(max_length=4,default='')


class data_point(models.Model):
	''' 数据体中的数据点'''
	model_name = models.ForeignKey(ProductModelName,default='')
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

class Deviceinfo(models.Model):
	'''设备信息'''
	model_name = models.ForeignKey(ProductModelName,default='')
	UUID = models.CharField(max_length=24,blank=True)
	device_name = models.CharField(max_length=64,blank=True)
	device_class = models.CharField(max_length=64,blank=True)
	create_time = models.DateTimeField(auto_now=True,blank=True)
		
class AddDeciveDataTable():
	'''添加设备日记表'''
	def __init__(self,table_name):
		self.table_name = str(table_name)+'_'+'Data'

	def create_table(self):
		'''创建数据表'''
		sql_cmd = 'CREATE TABLE IF NOT EXISTS {} ( id int(11) NOT NULL AUTO_INCREMENT,UUID varchar(24) NOT NULL,Currenttime datetime NOT NULL,PRIMARY KEY (id))ENGINE=InnoDB DEFAULT CHARSET=utf8;'.format(self.table_name)
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

class DeviceStatus(models.Model):
	'''设备状态'''
	UUID = models.CharField(max_length=24,blank=True)
	status = models.CharField(max_length=1,blank=True)
	info = models.CharField(max_length=10,blank=True)
	currenttime =  models.DateTimeField(auto_now=True,blank=True)




