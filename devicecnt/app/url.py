from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Login.UserLogin,name='UserLogin'),
    url(r'^Signup$',views.Login.UserSignup,name='Signup'),
    url(r'^Keyback$',views.Login.UserKeyback,name='Keyback'),
    url(r'^Logout/$',views.Login.UserLogout,name='UserLogout'),
    url(r'^Restkey/$',views.Login.UserRestKey,name='UserRestKey'),
    url(r'^Signup_auth/$',views.Login.Signup_auth,name='Signup_auth'),
    url(r'^UserLogout/$',views.Login.UserLogout,name='UserLogout')
]