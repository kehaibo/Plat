#coding:utf-8
import json

from . import config

from django.conf import settings

from django.urls import reverse

from django.shortcuts import HttpResponse,render,redirect

from django.contrib.auth import authenticate,login,logout 

from django.contrib.auth.models import User as auth_User

from django.contrib.auth.decorators import login_required

from django.db.utils import IntegrityError

from .form import ForgetForm,ResetForm,SignUpForm

from django.core.mail import EmailMultiAlternatives,BadHeaderError

from django.http import Http404,JsonResponse
    

#登录
class Login:

	Restkey_url='/login/Restkey'#重置密码URL
	signup_authurl='/login/Signup_auth'
	usermail=''#用户邮件名
	restkey=''#重置密码成功标记
	signupkey=False#注册密码标记，用于标记已经注册成功的用户，不能再次访问注册链接
	userinfo={
		'username':'',
		'email':'',
		'password':''
	}
	#重置密码
	def UserRestKey(request):
		if Login.restkey==True:
			raise Http404
		else:
			if request.method == 'POST':
				res = ResetForm(request.POST)
				if res.is_valid():
					try:
						User=auth_User.objects.get(email=Login.usermail)
					except Exception as e:
						raise Http404
					else:	
						User.set_password(res['newpwd1'].value())
						User.save()
						Login.restkey = True
						return render(request,"keyback_email.html",{'form':res,'restkey':Login.restkey})
				else:
					return render(request,"keyback_email.html",{'form':res})
			else:
				res=ResetForm()
				return render(request,"keyback_email.html",{'form':res})
	#忘记密码
	def UserKeyback(request):

		if request.method == 'POST':

			forget = ForgetForm(request.POST)

			if forget.is_valid():

				try:
					subject,Login.usermail = '忘记密码', forget['email'].value()
					try:
						User=auth_User.objects.get(email=Login.usermail)
					except Exception as e:
						user_exist=False
						return render(request,"keyback.html",{'form':forget,'user_exist':user_exist})
					else:
						text_content=''
						html_content = "<a href='http://{}{}'> 请点击这里重置密码 </a>".format(request.get_host(),Login.Restkey_url)
						Login.send_email(subject,settings.EMAIL_HOST_USER,[Login.usermail],text_content,html_content)
						return HttpResponse('发送成功')

				except BadHeaderError:#防止标头注入安全漏洞
					return HttpResponse('无效的标头')
			
			else:
				return render(request,"keyback.html",{'form':forget})

		else:

			forget = ForgetForm()

		return render(request,"keyback.html",{'form':forget})

	#用户注册邮件认证
	def Signup_auth(request): 

		if Login.signupkey == False:
		
			if request.method == 'GET':

				if Login.userinfo.get('username'):
					try:
						user = auth_User.objects.create_user(**Login.userinfo)
					except Exception as e:
						print('创建用户失败'+str(e))
						create_user = False
						return render(request,"sigupsuccess.html",{'create_user':create_user})
					else:
						return render(request,"sigupsuccess.html")
				else:
					raise Http404
				Login.signupkey=True
		else:
			return HttpResponse('404')


	#用户注册
	def UserSignup(request):
		
		dicts={}

		if request.is_ajax():#ajax 提交的，后台无法重定向
			body = json.loads(request.body)
			if auth_User.objects.filter(email=body['email']).exists():
				dicts["email_used"]=True
				return JsonResponse(dicts)
			elif auth_User.objects.filter(username=body['username']).exists():
				dicts["username_used"]=True
				return JsonResponse(dicts)
			else:
				try:
					subject='注册信息认证'
					text_content='注册信息认证'
					#html = '<p>This is an <strong>important</strong> message.</p>'
					with open(config.signup_email_html,'r',encoding='utf-8') as f:
						html = r'{}'.format(f.read())
						html = html.format(request.get_host(),Login.signup_authurl)
					Login.send_email(subject,settings.EMAIL_HOST_USER,[body['email']],text_content,html)
				except Exception as e: 
					print('邮件发送失败'+str(e))
					dicts['except']=str(e)
					return JsonResponse(dicts)
				else:
					Login.userinfo['username']=body['username']
					Login.userinfo['email']=body['email']
					Login.userinfo['password']=body['password']
					dicts['created']=True
					return JsonResponse(dicts)
				#user.save()		
		else:
			return render(request,"signup.html")

	def single_page(request,templates_name):
		'''用于返回单页面的通用视图函数 '''
		return render(request,templates_name)

	#用户登录
	def UserLogin(request):

		if request.method == "POST":
			
			username = request.POST.get("username")

			password = request.POST.get("password")

			user = authenticate(username=username,password=password)

			if user is not None and user.is_active:

				login(request,user)

				return redirect('/device/home')

			else :

				context={'login_error':True}

				return render(request,"login.html",{'context':context})

		return render(request,"login.html")

	def send_email(subject,from_email,to_email,text_content,html_content):
		'''subject:邮件主题；from_email：发送邮件的邮箱地址;to_email:接收邮件地址
			text_content：文本格式邮件内容;html_content：html格式邮件内容'''
		try:
			msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)#EmailMultiAlternatives 该类就可以发送文本也可以发送html
			msg.attach_alternative(html_content,"text/html")#发送html
			msg.send()
		except BadHeaderError:#防止标头注入安全漏洞
			raise BadHeaderError 
		except Exception as e:
			raise e

	#用户退出
	def UserLogout(request):

		logout(request)

		return redirect("/login/")

