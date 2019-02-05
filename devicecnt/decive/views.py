import json
import datetime
from django.http import Http404,JsonResponse
from django.shortcuts import render,redirect
from .comm import TypeConvert,data_type_list,mysqldatabasename
from django.db.models import Q  #Q类用于使用 | & ^ 逻辑 条件
from decive.models import *
#ProductModelName,data_point,upstream,downstream,AddDeciveDataTable,upstream_datapoint,downstream_datapoint,Deviceinfo,DeviceStatus
from django.contrib.auth.models import User as auth_User
from django.contrib.auth.decorators import login_required
import time,hashlib
from django.db import connection
#from .tasks import * 


# Create your views here.
class device:

	@login_required
	def home(request):
		'''主页'''  
		return render(request,'home.html',{'username':request.user,'online':'online'})

	@login_required
	def product_development(request):
		'''产品开发'''
		ProductModelobj=ProductModelName.objects.filter(user_id=str(request.user))#获取历史
		if request.is_ajax():
			data = json.loads(request.body)
			product_model = str(request.user)+'_'+str(data['product_model'])
			
			if ProductModelName.objects.filter(product_model=product_model).exists():
				return JsonResponse({'exists':True})
			else:
				#创建新产品模型
				p = ProductModelName(product_model=product_model,product_desc=data['product_dec'],user_id=str(request.user))#把获取到的主键id作为产品模型的外键
				p.save()
				AddDeciveDataTable(product_model).create_table()
				print()
				#return render(request,'product_development.html',{'username':device.user_logined,'online':'offline'})
				return JsonResponse({'success':'success'})
		return render(request,'product_development.html',{'username':request.user,'online':'online','ProductModelobj':ProductModelobj})

	@login_required
	def del_model(request):
		'''删除模型'''
		if request.is_ajax():
			data = json.loads(request.body)
			model_name = data['model_name']
			del_Modelobj=ProductModelName.objects.filter(product_model=model_name)
			if del_Modelobj.exists():
				del_Modelobj.delete()
				AddDeciveDataTable(model_name).remove_table()
			return JsonResponse({'success':'success'})
		return redirect('/device/product_development')

	@login_required
	def product_development_model(request,model_name):
		'''模型具体定义中的初次加载页面'''
		if request.is_ajax():
			return JsonResponse({'SUCCESS':'SUCCESS'})			
		ProductModelobj=ProductModelName.objects.get(product_model=model_name)
		ExistsedPointlist=data_point.objects.filter(model_name__product_model=model_name)#双下划线可进行外键查询
		upstreamlist     = upstream.objects.filter(model_name__product_model=model_name)
		downstreamlist     = downstream.objects.filter(model_name__product_model=model_name)
		upstream_datapointlist = upstream_datapoint.objects.filter(model_name__product_model=model_name)
		downstream_datapointlist = downstream_datapoint.objects.filter(model_name__product_model=model_name)
		return render(request,'product_development_specific.html',{'username':request.user,'online':'online',
					'ProductModelobj':ProductModelobj,'ExistsedPointlist':ExistsedPointlist,
					'upstreamlist':upstreamlist,'downstreamlist':downstreamlist,
					'upstream_datapointlist':upstream_datapointlist,
					'downstream_datapointlist':downstream_datapointlist,
					},)
	
	@login_required
	def product_development_specific(request,model_name,uri):	
		if request.is_ajax():
			if uri=='databody':
				if request.method == 'POST':
					point=json.loads(request.body)	
					modelqueryset = ProductModelName.objects.filter(product_model=model_name)
					modelqueryset.update(current_time=datetime.datetime.now().isoformat())	
					get_model = modelqueryset[0]		
					if  point['Operation_type'] == 'save':
						'''保存数据点'''
						data_type=TypeConvert(point['data_type'])

						if data_type in data_type_list['number'].values():
							data_pointobj=data_point(data_name=point['data_name'],show_name=point['show_name'],
											TLV_Type=point['TLV_Type'],operation_type=point['operation_type'],
											data_type=data_type,max_value=point['max_value'],
											min_value=point['min_value'],step_by_step=point['step_by_step'],
											value_unit=point['value_unit'],model_name=get_model)
							data_pointobj.save()

						elif data_type in data_type_list.values():
							if data_type=='HexStr' or data_type=='UTF8Str':
								data_pointobj=data_point(data_name=point['data_name'],show_name=point['show_name'],
												TLV_Type=point['TLV_Type'],operation_type=point['operation_type'],
												data_type=data_type,str_maxlen=point['str_maxlen'],model_name=get_model)
								data_pointobj.save()
							else:
								data_pointobj=data_point(data_name=point['data_name'],show_name=point['show_name'],
												TLV_Type=point['TLV_Type'],operation_type=point['operation_type'],
												data_type=data_type,true_value_name=point['true_value_name'],
												true_value_show=point['true_value_show'],true_bool_value=point['true_bool_value'],
												false_value_name=point['false_value_name'],false_value_show=point['false_value_show'],
												false_bool_value=point['false_bool_value'],str_maxlen=point['str_maxlen'],model_name=get_model)
								data_pointobj.save()
						else:
							raise ('data_type error')   #数据类型不在对照表内的产生异常

						AddDeciveDataTable(model_name).add_field(point['data_name']) 
						return JsonResponse({'success':'success'})

					elif  point['Operation_type'] == 'updatesave':
						''' 更新数据点 '''
						print('updatesave:'+str(point))
						data_type      = TypeConvert(point['data_type'])
						print(data_type)
						#，由外键指定的表来查询本表，通过外键反向查询xxxx_set，即可访问本表符合要求对象
						data_pointqset = get_model.data_point_set.filter(data_name=point['data_name'])
						#外键反向查询
						if data_type in data_type_list['number'].values():
							print(data_pointqset)
							try:
								data_pointqset.update(data_name=point['data_name'],show_name=point['show_name'],
												TLV_Type=point['TLV_Type'],operation_type=point['operation_type'],
												data_type=data_type,max_value=point['max_value'],
												min_value=point['min_value'],step_by_step=point['step_by_step'],
												value_unit=point['value_unit'],model_name=get_model)
							except Exception as e:
								print(e)

						elif data_type in data_type_list.values():
							if data_type=='HexStr' or data_type=='UTF8Str':
								data_pointqset.update(data_name=point['data_name'],show_name=point['show_name'],
												TLV_Type=point['TLV_Type'],operation_type=point['operation_type'],
												data_type=data_type,str_maxlen=point['str_maxlen'],model_name=get_model)
							else:
								data_pointqset.update(data_name=point['data_name'],show_name=point['show_name'],
												TLV_Type=point['TLV_Type'],operation_type=point['operation_type'],
												data_type=data_type,true_value_name=point['true_value_name'],
												true_value_show=point['true_value_show'],true_bool_value=point['true_bool_value'],
												false_value_name=point['false_value_name'],false_value_show=point['false_value_show'],
												false_bool_value=point['false_bool_value'],str_maxlen=point['str_maxlen'],model_name=get_model)
						
						else:
							raise ('data_type error')   #数据类型不在对照表内的产生异常

						return JsonResponse({'success':'success'})


					else:#point['Operation_type'] == 'del'#删除数据点
						DataPointObj = data_point.objects.get(model_name=get_model,data_name=point['datapoint_name'])
						DataPointObj.delete()
						AddDeciveDataTable(model_name).remove_field(point['datapoint_name']) 
						return JsonResponse({'success':'success'})

			elif uri=='updata':
				''' 上行数据业务'''
				if request.method == 'POST':
					'''post'''
					point=json.loads(request.body)
					print(point)
					modelqueryset  = ProductModelName.objects.filter(product_model=model_name)
					modelqueryset.update(current_time=datetime.datetime.now().isoformat())
					get_model=modelqueryset[0] #模型实例

					if point['operation'] == 'save':

						try:

							upstreamqst    = upstream(model_name=get_model,stream_showname=point['stream_showname'],
																				stream_name=point['stream_name'],
																				stream_Type=point['stream_Type'],
																				)									
							upstreamqst.save()
							return JsonResponse({'success':'success'})
						except Exception as e:
							print(e)
						#get_datapoint = get_model.data_point_set.get(show_name=point['upstream_point'])
						#upstreamqst.up_point.add(get_datapoint.id)#数据点与上行数据建立多对多关系
					elif point['operation'] == 'del':
						'''删除数据点'''
						#print(point)
						try:
							streamobj = upstream.objects.get(model_name=get_model,stream_name=point['stream_name'])
							streamobj.delete()
							return JsonResponse({'success':'success'})
						except Exception as e:
							print('del stream error'+str(e))
							return JsonResponse({'error':'error'})

					elif point['operation'] == 'update_info':
						'''更新数据体信息'''
						try:
							streamobj = upstream.objects.filter(id=point['stream_id'])
							streamobj.update(model_name=get_model,stream_showname=point['stream_showname'],
																				stream_name=point['stream_name'],
																				stream_Type=point['stream_Type'],)
							return JsonResponse({'success':'success'})
						except Exception as e:
							print('update stream error'+str(e))
							return JsonResponse({'error':'error'})

					elif point['operation'] == 'update_point':
						'''更新数据流中的数据点'''
						#print(point)
						try:
							streamobj = upstream.objects.get(model_name=get_model,stream_name=point['stream_name'])
							if upstream_datapoint.objects.filter(upstream=streamobj).exists():
								for _instance in upstream_datapoint.objects.filter(upstream=streamobj):
									_instance.delete()
							
							for selectedpoint in point['selectedpoint']:
								selectedpoint_ins = data_point.objects.get(model_name=get_model,show_name=selectedpoint)
								upstreamdatapoint_ins = upstream_datapoint(model_name=get_model,upstream=streamobj,
																			data_point=selectedpoint_ins,
																			point_attr=point['point_attr'])
								upstreamdatapoint_ins.save()
							return JsonResponse({'success':'success'})
						except Exception as e:
							print('error:save upstream datapoint failed! {}'.format(e))
							return JsonResponse({'error':'error'})	

			elif uri=='downdata':
				if request.method == 'POST':
					point=json.loads(request.body)
					#print(point)
					modelqueryset  = ProductModelName.objects.filter(product_model=model_name)
					modelqueryset.update(current_time=datetime.datetime.now().isoformat())
					get_model=modelqueryset[0] #模型实例

					if point['operation'] == 'save':
						try:
							downstream_ins = downstream(model_name=get_model,stream_showname=point['stream_showname'],
																					stream_name=point['stream_name'],
																					stream_Type=point['stream_Type'],
																					)	
							downstream_ins.save()
							return JsonResponse({'success':'success'})
						except Exception as e:
							print('error:save downstream {}'.format(e))
							return JsonResponse({'error':'error'})	
					elif point['operation'] == 'del':
						try:
							streamobj = downstream.objects.get(model_name=get_model,stream_name=point['stream_name'])
							streamobj.delete()
							return JsonResponse({'success':'success'})
						except Exception as e:
							print('del stream error'+str(e))
							return JsonResponse({'error':'error'})	

					elif point['operation'] == 'update_info':
						try:
							streamobj = downstream.objects.filter(id=point['stream_id'])
							streamobj.update(model_name=get_model,stream_showname=point['stream_showname'],
																				stream_name=point['stream_name'],
																				stream_Type=point['stream_Type'],)
							return JsonResponse({'success':'success'})
						except Exception as e:
							print('update stream error'+str(e))
							return JsonResponse({'error':'error'})

					elif point['operation'] == 'update_point':
						'''更新下行数据点及响应数据点'''
						try:
							streamobj = downstream.objects.get(model_name=get_model,stream_name=point['stream_name'])
							if downstream_datapoint.objects.filter(downstream=streamobj).exists():
								for _instance in downstream_datapoint.objects.filter(downstream=streamobj,point_attr=point['point_attr']):
									_instance.delete()
							
							for selectedpoint in point['selectedpoint']:
								selectedpoint_ins = data_point.objects.get(model_name=get_model,show_name=selectedpoint)
								downstreamdatapoint_ins = downstream_datapoint(model_name=get_model,downstream=streamobj,
																			data_point=selectedpoint_ins,
																			point_attr=point['point_attr'])
								downstreamdatapoint_ins.save()
							return JsonResponse({'success':'success'})
						except Exception as e:
							print('error:save upstream datapoint failed! {}'.format(e))
							return JsonResponse({'error':'error'})	

			elif uri=='basic':
				return JsonResponse({'success':'success'})

	@login_required
	def device_management(request):
		''' 设备管理'''
		if request.is_ajax():
			if request.method == "POST":
				device_informations=json.loads(request.body)
				if device_informations['operation'] == 'create':
					get_model = ProductModelName.objects.get(product_model=device_informations['device_product'])
					md5obj = hashlib.md5(str(time.clock()).encode('utf-8'))
					UUID = md5obj.hexdigest().upper()
					deviceobj = Deviceinfo(model_name=get_model,
											device_name=device_informations['device_name'],
											device_desc=device_informations['device_dec'],
											device_user_id=str(request.user),
											UUID=UUID,
											)
					deviceobj.save()
					Devicedefault_status = DeviceStatus(UUID=UUID,status='0',info='离线',device=deviceobj)
					Devicedefault_status.save() #设备默认为离线状态
					#print(device_informations)
					return JsonResponse({'success':'success'})
				elif device_informations['operation'] == 'update':
					print(device_informations)
					get_model = ProductModelName.objects.get(product_model=device_informations['device_product'])
					deviceobj = Deviceinfo.objects.filter(UUID=device_informations['device_uuid'])
					deviceobj.update(model_name=get_model,
									device_name=device_informations['device_name'],
									device_desc=device_informations['device_dec'],
									UUID=device_informations['device_uuid'])
					return JsonResponse({'success':'success'})
				else:
					deviceobj = Deviceinfo.objects.filter(UUID=device_informations['device_uuid'])
					deviceobj.delete()
					device_statusobj = DeviceStatus.objects.filter(UUID=device_informations['device_uuid'])
					device_statusobj.delete()
					return JsonResponse({'success':'success'}) 
		else:
			ProductModelobj=ProductModelName.objects.filter(user_id=str(request.user))
			if request.method=='POST':
				#print(json.loads(request.body))
				#通过uuid进行模糊查询设备
				uuid_like ='%' + request.POST.get('uuid_four')+'%'
				page_number = 1
				devices_Info_Status = Deviceinfo.objects.raw("select * from django.decive_deviceinfo left join  ( select UUID,info from ( select * from django.decive_devicestatus order by id desc) AS DOWN group by UUID) AS NEW ON NEW.UUID = django.decive_deviceinfo.UUID AND django.decive_deviceinfo.device_user_id = %s AND  django.decive_deviceinfo.UUID LIKE %s WHERE NEW.info is not NULL; ",[str(request.user),uuid_like])
				try:
					total_page_number = len(list(devices_Info_Status))//10 + (len(list(devices_Info_Status))%10)/(len(list(devices_Info_Status))%10)
				except Exception as e:
					total_page_number =len(list(devices_Info_Status))//10 
				return render(request,'device_management.html',{'username':request.user,'online':'online',
						'ProductModelobj':ProductModelobj,'devices_Info_Status':devices_Info_Status,'page_number':page_number,'total_page_number':int(total_page_number)})
			else:
				#前10个设备的信息与状态	
				devices_Info_Status = Deviceinfo.objects.raw("select * from django.decive_deviceinfo left join  ( select UUID,info from ( select * from django.decive_devicestatus order by id desc) AS DOWN group by UUID) AS NEW ON NEW.UUID = django.decive_deviceinfo.UUID AND django.decive_deviceinfo.device_user_id = %s WHERE NEW.info is not NULL;",[str(request.user)])
				try:
					total_page_number = len(list(devices_Info_Status))//10 + (len(list(devices_Info_Status))%10)/(len(list(devices_Info_Status))%10)
				except Exception as e:
					total_page_number =len(list(devices_Info_Status))//10 
				page_number = 1
				return render(request,'device_management.html',{'username':request.user,'online':'online',
							'ProductModelobj':ProductModelobj,'devices_Info_Status':devices_Info_Status[0:10],'page_number':page_number,'total_page_number':int(total_page_number)})

	@login_required
	def device_details(request,device_uuid):
		'''单个设备详情,包括设备详细信息，原始JSON和16进制数据展示以及历史命令状态'''
		device = Deviceinfo.objects.raw("select * from django.decive_deviceinfo left join  ( select UUID,info from ( select * from django.decive_devicestatus order by id desc) AS DOWN group by UUID) AS NEW ON NEW.UUID = django.decive_deviceinfo.UUID AND django.decive_deviceinfo.device_user_id = %s AND  django.decive_deviceinfo.UUID LIKE %s WHERE NEW.info is not NULL; ",[str(request.user),device_uuid])
		model_id = Deviceinfo.objects.get(UUID=device_uuid).model_name_id
		model_name = ProductModelName.objects.get(id=model_id).product_model
		HistoryDateTable = str(model_name)+'_'+'Data'
		get_columns_name_sqlcmd = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '{}' and table_schema='{}' ".format(HistoryDateTable,mysqldatabasename)
		get_history_data_sqlcmd = "select * from {} where UUID = '{}' ".format(HistoryDateTable,device_uuid)
		with connection.cursor() as cursor:#获取数据表字段名
			cursor.execute(get_columns_name_sqlcmd)
			ColumnsName = cursor.fetchall()
		with connection.cursor() as cursor:#获取数据表数据
			cursor.execute(get_history_data_sqlcmd)
			HistoryData = cursor.fetchall()
		#字段名与值 组合成json(字典)格式用于展示
		HistoryDatalist = list()
		for i,datas in enumerate(HistoryData):
			HistoryDatedict = dict()
			for index,data in enumerate(datas):
				HistoryDatedict[ColumnsName[index][0]] = data
			HistoryDatalist.append(HistoryDatedict)
		return render(request,'device_details.html',{'username':request.user,'online':'online','device':device[0],'HistoryDatalist':HistoryDatalist})
	
	@login_required
	def device_management_page(request,page_number):
		'''设备分页展示,每页只展示10个设备'''
		page_number = int(page_number)
		max_index=int(page_number)*10
		min_index=int(page_number)*10-10 
		ProductModelobj=ProductModelName.objects.filter(user_id=str(request.user))
		devices_Info_Status = Deviceinfo.objects.raw("select * from django.decive_deviceinfo left join  ( select UUID,info from ( select * from django.decive_devicestatus order by id desc) AS DOWN group by UUID) AS NEW ON NEW.UUID = django.decive_deviceinfo.UUID AND django.decive_deviceinfo.device_user_id = %s order by id ",[str(request.user)])
		try:
			total_page_number = len(list(devices_Info_Status))//10 + (len(list(devices_Info_Status))%10)/(len(list(devices_Info_Status))%10)
		except Exception as e:
			total_page_number =len(list(devices_Info_Status))//10 
		return render(request,'device_management.html',{'username':request.user,'online':'online',
					'ProductModelobj':ProductModelobj,'devices_Info_Status':devices_Info_Status[min_index:max_index],'page_number':page_number,'total_page_number':int(total_page_number)})


	@login_required
	def device_testing(request):
		'''设备调试'''
		if request.is_ajax():
			if request.method == 'POST':
				data =json.loads(request.body) #正式是json格式
				#re = add.apply_async((1,1),countdown=1000,serializer='json')
				#print(re)
				return JsonResponse({'success':'success'})
		devices = Deviceinfo.objects.filter(device_user_id=str(request.user))
		return render(request,'device_testing.html',{'username':request.user,'online':'online','devices':devices,})

	@login_required
	def simulation_device(request):
		'''模拟设备'''
		return render(request,'simulation_device.html',{'username':request.user,'online':'online',})
	
	@login_required
	def product_show(request):
		'''产品展示'''
		return render(request,'product_show.html',{'username':request.user,'online':'online',})
