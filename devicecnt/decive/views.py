import json
import datetime
from django.http import Http404,JsonResponse
from django.shortcuts import render,redirect
from .comm import TypeConvert,data_type_list
from decive.models import ProductModelName,data_point,stream,AddDeciveDataTable
from django.contrib.auth.models import User as auth_User
from django.contrib.auth.decorators import login_required

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
		Upstreamlist     = stream.objects.filter(model_name__product_model=model_name)
		print(Upstreamlist.all())
		return render(request,'product_development_specific.html',{'username':request.user,'online':'online',
					'ProductModelobj':ProductModelobj,'ExistsedPointlist':ExistsedPointlist,'Upstreamlist':Upstreamlist})
	
	@login_required
	def product_development_specific(request,model_name,select):	
		if request.is_ajax():
			if select=='databody':
				if request.method == 'POST':
					point=json.loads(request.body)					
					if  point['Operation_type'] == 'save':
						'''保存数据点'''
						data_type=TypeConvert(point['data_type'])
						modelqueryset = ProductModelName.objects.filter(product_model=model_name)
						get_model = ProductModelName.objects.get(product_model=model_name)
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
						modelqueryset.update(current_time=datetime.datetime.now().isoformat())
						return JsonResponse({'success':'success'})

					elif  point['Operation_type'] == 'update_save':
						''' 更新数据点 '''
						print('update-save:'+str(point))
						data_type      = TypeConvert(point['data_type'])
						modelqueryset  = ProductModelName.objects.filter(product_model=model_name)
						#，由外键指定的表来查询本表，通过外键反向查询xxxx_set，即可访问本表符合要求对象
						get_model      = ProductModelName.objects.get(product_model=model_name)
						data_pointqset = get_model.data_point_set.filter(data_name=point['data_name'])
						#外键反向查询
						if data_type in data_type_list['number'].values():
							data_pointqset.update(data_name=point['data_name'],show_name=point['show_name'],
											TLV_Type=point['TLV_Type'],operation_type=point['operation_type'],
											data_type=data_type,max_value=point['max_value'],
											min_value=point['min_value'],step_by_step=point['step_by_step'],
											value_unit=point['value_unit'],model_name=get_model)

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

						modelqueryset.update(current_time=datetime.datetime.now().isoformat())
						return JsonResponse({'success':'success'})


					else:#point['Operation_type'] == 'del'#删除数据点
						DataPointObj = data_point.objects.get(data_name=point['datapoint_name'])
						DataPointObj.delete()
						AddDeciveDataTable(model_name).remove_field(point['data_name']) 
						return JsonResponse({'success':'success'})

			elif select=='updata':
				''' 上行数据业务'''
				if request.method == 'POST':
					'''post'''
					point=json.loads(request.body)

					if point['operation'] == 'save':
						get_model      = ProductModelName.objects.get(product_model=model_name)
						
						upstreamqst    = stream(model_name=get_model,upstream_showname=point['upstream_showname'],
													upstream_name=point['upstream_name'],upstream_point=point['upstream_point'],upstream_Type=point['upstream_Type'])

						upstreamqst.save()
						
						#get_datapoint = get_model.data_point_set.get(show_name=point['upstream_point'])
						#upstreamqst.up_point.add(get_datapoint.id)#数据点与上行数据建立多对多关系
						return JsonResponse({'success':'success'})
					


				return JsonResponse({'success':'success'})
			elif select=='downdata':
				return JsonResponse({'success':'success'})
			elif select=='basic':
				return JsonResponse({'success':'success'})

		
	def device_management(request):
		''' 设备管理'''
		pass

	def device_testing(request):
		'''设备调试'''
		pass

	def simulation_device(request):
		'''模拟设备'''
		pass
	def product_show(request):
		'''产品展示'''
		pass
