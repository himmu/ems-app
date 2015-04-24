from django.shortcuts import render,render_to_response,RequestContext,HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import Context, RequestContext
from models import *
import random
import string
import shutil
import os
from django.core import mail 
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string,get_template
from django.core.mail import EmailMultiAlternatives

# Create your views here.

def user_login_required(f):
		def wrap(request, *args, **kwargs):
		#this check the session if userid key exist, if not it will redirect to login page
			if 'user_session' not in request.session.keys():
				content={}
				content['message']="You are already Logout"
			  	return HttpResponseRedirect("/index",content)
			return f(request, *args, **kwargs)
		wrap.__doc__=f.__doc__
		wrap.__name__=f.__name__
		return wrap


def login(request):
	content={}
	content.update(csrf(request))

	if request.method=="POST":
		username=request.POST['username']
		password=request.POST['pass']
		try:
			user_detail_obj=Registered_Employee_Detail.objects.get(emp_email=username,emp_password=password)

		except:
			content['unsuccess_message']="Please Register first for login."
			return render_to_response("index.html",content,context_instance=RequestContext(request))
		if user_detail_obj.is_verified==True:

			if user_detail_obj.emp_role=="Admin":

				request.session['user_session']=username
				session=request.session['user_session']
				print session
				return HttpResponseRedirect("admin_index")
			elif user_detail_obj.emp_role=="User":
				request.session['user_session']=username
				session=request.session['user_session']
				print session
				return HttpResponseRedirect("/user_index")
		else:
			content['unsuccess_message']="Sorry! you han'nt verified your email account please verify"
	return render_to_response("index.html",content,context_instance=RequestContext(request))

# @user_login_required
def adduser(request):
	
	content={}
	
	content.update(csrf(request))
	str1="wert5y6u7iopasdfghjklzxcvbnm"
	str2="zxcvbnmasdfghjklqwertyuiop"
	str3="asdfghjklqwertyuiopzxcvbnm"
	if request.method=="POST":
		emp_id=random.choice(str1)+random.choice(str2)+random.choice(str3)+str(random.randint(0,200))
		emp_first_name=request.POST['fname']
		emp_middle_name=request.POST['mname']
		emp_last_name=request.POST['lname']
		emp_full_name=emp_first_name+emp_middle_name+emp_last_name
		emp_email=request.POST['email']
		emp_password=request.POST['password']
		emp_address=request.POST['address']
		emp_gender=request.POST['gender']
		emp_marital_status=request.POST['marriage']
		emp_contact_number=request.POST['phone']
		emp_role=request.POST['employeerole']
		
		regss_obj=Registered_Employee_Detail.objects.create(emp_id=emp_id,emp_first_name=emp_first_name,emp_middle_name=emp_middle_name,emp_last_name=emp_last_name,emp_full_name=emp_full_name,emp_email=emp_email,emp_password=emp_password,emp_address=emp_address,emp_gender=emp_gender,emp_marital_status=emp_marital_status,emp_contact_number=emp_contact_number,emp_role=emp_role)
		filter_details=Registered_Employee_Detail.objects.filter(emp_email=emp_email)
		content['username']=filter_details[0].emp_email
		content['password']=filter_details[0].emp_password
		content['firstname']=filter_details[0].emp_first_name
		content['verification_code']=filter_details[0].emp_id		
		if regss_obj:
			subject="Account Confirmation"
			
			
			message=render_to_string("signupmail.txt",content)
			to=[emp_email]
			by="avishek@anipr.in"
			EmailMessage(subject,message,to=to,from_email=by).send()
		
			return render_to_response("verify.html",content)
			


		# Admin.objects.filter(emp_id=reg_obj[0].emp_id).update(emp_role=emp_role)

		return render_to_response("index.html",content)
	return render_to_response("index.html",content,context_instance=RequestContext(request))


@user_login_required
def logout(request):
	content ={}
	session=request.session['user_session']
	
	print session
	del request.session['user_session']
	print session
	return render_to_response("index.html",content,context_instance=RequestContext(request))

def forgetpassword(request):
	content={}
	content.update(csrf(request))

	return render_to_response("forgetpassword.html",content,context_instance=RequestContext(request))

def password_mail(request):
	content={}
	content.update(csrf(request))

	if request.method=="POST":
		email=request.POST['email']
		user_detail_obj=Registered_Employee_Detail.objects.filter(emp_email=email)
		user_detail_obj[0].emp_password
		user_detail_obj[0].emp_email
		user_detail_obj[0].emp_first_name
		subject="Password recovery"
		message="Hi "+user_detail_obj[0].emp_first_name +" How's the day Your Password : "+user_detail_obj[0].emp_password
		send_mail(subject,message,"avishek@anipr.in",[user_detail_obj[0].emp_email])
	return render_to_response("index.html",content,context_instance=RequestContext(request))

@user_login_required
def resetpassword(request):
	content={}
	content.update(csrf(request))
	session=request.session['user_session']
	if request.method=="POST":
		newpass=request.POST['pass']
		repass=request.POST['rpass']
		if newpass==repass:
			Registered_Employee_Detail.objects.filter(emp_email=session).update(emp_password=newpass)
			content['message']="Password successfully updated"
			return render_to_response("users/index.html",content,context_instance=RequestContext(request))
		content['message']="Password does'nt match please re-enter"
		return render_to_response("reset.html",content,context_instance=RequestContext(request))
	return render_to_response("reset.html",content,context_instance=RequestContext(request))




def admin_index(request):
	content={}
	content.update(csrf(request))
	return render_to_response("Admin/index.html",content,context_instance=RequestContext(request))


def user_index(request):
	
	content={}
	content.update(csrf(request))
	return render_to_response("users/index.html",content,context_instance=RequestContext(request))


def verify(request):
	content={}
	content.update(csrf(request))
	if request.method=="POST":
		email=request.POST['email']
		v_code=request.POST['verify']
		user_detail_obj=Registered_Employee_Detail.objects.filter(emp_email=email)
		if v_code==user_detail_obj[0].emp_id:
			Registered_Employee_Detail.objects.filter(emp_email=email).update(is_verified=True)
			content['success_message']="Your Email is Successfully verified, Now you can Login"
			return render_to_response("index.html",content,context_instance=RequestContext(request))
		else:
			content['unsuccess_message']="Verification code is invalid please try again with valid code"
			return render_to_response("verify.html",content,context_instance=RequestContext(request))
	return render_to_response("verify.html",content,context_instance=RequestContext(request))


