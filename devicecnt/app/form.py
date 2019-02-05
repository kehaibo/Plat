from django import forms
from captcha.fields import CaptchaField


class SignUpForm(forms.Form):# 用户注册信息username,password,confirm_password,email
	name=forms.CharField(required=True,label="用户名称")
	email=forms.EmailField(required=True,label="用户邮箱") #email 字段
	pword=forms.CharField(required=True,min_length=6,label='输入密码',error_messages={'required':'密码不能为空','min_length':'密码长度至少6位'})


#验证邮箱格式和验证码
class ForgetForm(forms.Form):
	email=forms.EmailField(required=True) #email 字段
	captcha=CaptchaField(error_messages={'invalid':'验证码错误,请重新填写'},label='验证码')#验证码字段

#验证新设的密码长度是否达标
class ResetForm(forms.Form):
	newpwd1=forms.CharField(required=True,min_length=6,label='请输入新密码',error_messages={'required':'密码不能为空','min_length':'密码长度至少6位'})
	newpwd2=forms.CharField(required=True,min_length=6,label='请确认新密码',error_messages={'required':'密码不能为空','min_length':'密码长度至少6位'})

