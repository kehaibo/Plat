from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^home/$', views.device.home,name='home'),
    url(r'^product_development/$', views.device.product_development,name='product_development'),
    url(r'^product_model/(?P<model_name>\w+)/$', views.device.product_development_model,name='product_development_model'),
    url(r'^product_development_specific/(?P<model_name>\w+)/(?P<select>\w+)/$', views.device.product_development_specific,name='product_development_specific'),
    url(r'^device_management/$', views.device.device_management,name='device_management'),
    url(r'^device_testing/$', views.device.device_testing,name='device_testing'),
    url(r'^simulation_device/$', views.device.simulation_device,name='simulation_device'),
    url(r'^del_model/$',views.device.del_model,name='del_model'),
]