from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/$', views.device.home,name='home'),
    url(r'^product_development/$', views.device.product_development,name='product_development'),
    url(r'^product_model/(?P<model_name>\w+)/$', views.device.product_development_model,name='product_development_model'),
    url(r'^product_development_specific/(?P<model_name>\w+)/(?P<uri>\w+)/$', views.device.product_development_specific,name='product_development_specific'),
    url(r'^device_management/$', views.device.device_management,name='device_management'),
   	url(r'^device_details/(?P<device_uuid>\w+)/$',views.device.device_details,name='device_details'),
    url(r'^device_testing/$', views.device.device_testing,name='device_testing'),
    url(r'^simulation_device/$', views.device.simulation_device,name='simulation_device'),
    url(r'^product_show/$', views.device.product_show,name='product_show'),
    url(r'^del_model/$',views.device.del_model,name='del_model'),
    url(r'^device_management/(?P<page_number>\w+)/$',views.device.device_management_page,name='device_management_page'),
]