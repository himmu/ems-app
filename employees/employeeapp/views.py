from django.shortcuts import render,render_to_response,RequestContext,HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import Context, RequestContext
from models import *
import random
import string
from random import randint
import os
from django.core import mail 
from django.http import HttpResponse
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings as conf_settings
import reportlab
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Image,Table
from reportlab.lib.colors import HexColor
from django.http import Http404,HttpResponseNotFound

# Decprators for preventing unauthorized  user
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

# for login functionality
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

# For adding the emplyees
def adduser(request):
	content={}
	
	content.update(csrf(request))
	str1="wert5y6u7iopasdfghjklzxcvbnm"
	str2="zxcvbnmasdfghjklqwertyuiop"
	str3="asdfghjklqwertyuiopzxcvbnm"
	if request.method=="POST":
		emp_id=random.choice(str1)+random.choice(str2)+random.choice(str3)+str(random.randint(0,200))
		emp_first_name=request.POST['fname']
		emp_last_name=request.POST['lname']
		emp_full_name=emp_first_name+" "+emp_last_name
		emp_email=request.POST['email']
		emp_password=request.POST['password']
		emp_address=request.POST['address']
		emp_gender=request.POST['gender']
		emp_marital_status=request.POST['marriage']
		emp_contact_number=request.POST['phone']
		emp_role=request.POST['employeerole']
		if 'profile_pic' in request.FILES:

			filee=request.FILES['profile_pic']
			if filee:
				file_name = str(randint(2,1000)) + filee.name
				regss_obj=Registered_Employee_Detail.objects.create(emp_id=emp_id,emp_first_name=emp_first_name,emp_last_name=emp_last_name,emp_full_name=emp_full_name,emp_email=emp_email,emp_password=emp_password,emp_address=emp_address,emp_gender=emp_gender,emp_marital_status=emp_marital_status,emp_contact_number=emp_contact_number,emp_role=emp_role,emp_profile_pic=file_name)

			
				
				data = filee.read()
				filee.close()
				filee = open(conf_settings.IMAGE_ROOT +file_name,"wb")
				filee.write(data)
				filee.close()
		else:
			regss_obj=Registered_Employee_Detail.objects.create(emp_id=emp_id,emp_first_name=emp_first_name,emp_last_name=emp_last_name,emp_full_name=emp_full_name,emp_email=emp_email,emp_password=emp_password,emp_address=emp_address,emp_gender=emp_gender,emp_marital_status=emp_marital_status,emp_contact_number=emp_contact_number,emp_role=emp_role)
		filter_details=Registered_Employee_Detail.objects.filter(emp_email=emp_email)
		content['verify_message']="We have sent verification code in your email adderss please verify your account"
		content['username']=filter_details[0].emp_email
		content['password']=filter_details[0].emp_password
		content['firstname']=filter_details[0].emp_first_name
		content['verification_code']=filter_details[0].emp_id		
		if regss_obj:
			subject="Account Confirmation"
			content=Context({"verification_code":filter_details[0].emp_id,"username":filter_details[0].emp_email,"password":filter_details[0].emp_password,"firstname":filter_details[0].emp_first_name})
			htmltemplate=get_template("htmlmessage.html")
			htmlt=htmltemplate.render(content)
			# message=render_to_string("signupmail.txt",content)
			to=[emp_email]
			by="avishek@anipr.in"
			# EmailMessage(subject,message,to=to,from_email=by).send()
			msg=EmailMultiAlternatives(subject,"",by,to)
			msg.attach_alternative(htmlt, "text/html") 
			msg.send() 
			return render_to_response("index.html",content)
			


		# Admin.objects.filter(emp_id=reg_obj[0].emp_id).update(emp_role=emp_role)

		return render_to_response("index.html",content,context_instance=RequestContext(request))
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



@user_login_required
def admin_index(request):
	content={}
	content.update(csrf(request))
	session=request.session['user_session']
	details=Registered_Employee_Detail.objects.filter(emp_email=session)
	content['firstname1']=details[0].emp_first_name
	content['profile_pic1']=details[0].emp_profile_pic
	# Counting number of user for admin dashboard
	details=Registered_Employee_Detail.objects.all().count()
	content['usercount']=details
	return render_to_response("Admin/index.html",content,context_instance=RequestContext(request))

@user_login_required
def user_index(request):
	
	content={}
	content.update(csrf(request))
	session=request.session['user_session']
	details=Registered_Employee_Detail.objects.filter(emp_email=session)
	content['firstname']=details[0].emp_first_name
	content['profile_pic']=details[0].emp_profile_pic
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


def ema(request):
	return render_to_response("htmlmessage.html")

@user_login_required
def fetch_users_for_admin(request):
	content={}
	session=request.session['user_session']
	content.update(csrf(request))
	current_user_detail=Registered_Employee_Detail.objects.filter(emp_email=session)

	content['profile_pic1']=current_user_detail[0].emp_profile_pic
	content['firstname1']=current_user_detail[0].emp_first_name
	alls=Registered_Employee_Detail.objects.all()
	# for i in alls:
	# 	print i.emp_gender
	content['user_det']=alls

	return render_to_response("Admin/generatelist.html",content,context_instance=RequestContext(request))



@user_login_required
def edit_user_by_admin(request):
	content={}
	session=request.session['user_session']
	current_user_detail=Registered_Employee_Detail.objects.filter(emp_email=session)

	content['profile_pic1']=current_user_detail[0].emp_profile_pic
	content['firstname1']=current_user_detail[0].emp_first_name
	if request.method=="GET":
		ids=request.GET['id']
		details=Registered_Employee_Detail.objects.filter(emp_id=ids)
		content['firstname']=details[0].emp_first_name
		content['lastname']=details[0].emp_last_name
		content['email']=details[0].emp_email
		content['password']=details[0].emp_password
		content['address']=details[0].emp_address
		content['gender']=details[0].emp_gender
		content['marry']=details[0].emp_marital_status
		content['phone']=details[0].emp_contact_number
		content['role']=details[0].emp_role
		content['profile_pic']=details[0].emp_profile_pic
		content['emp_id']=details[0].emp_id

		return render_to_response("Admin/edit_user.html",content,context_instance=RequestContext(request))

	elif request.method=="POST":
		emp_first_name=request.POST['fname']
		emp_last_name=request.POST['lname']
		emp_full_name=emp_first_name+" "+emp_last_name
		emp_email=request.POST['email']
		emp_password=request.POST['password']
		emp_address=request.POST['address']
		emp_gender=request.POST['gender']
		emp_marital_status=request.POST['marriage']
		emp_contact_number=request.POST['phone']
		emp_role=request.POST['employeerole']
		curr_image=request.POST['hide']
		print curr_image

		if 'profile_pic' in request.FILES:

			emp_profile_pic=request.FILES['profile_pic']
			if emp_profile_pic:
				file_name = str(randint(2,1000)) + emp_profile_pic.name
				data = emp_profile_pic.read()
				emp_profile_pic.close()
				filee = open(conf_settings.IMAGE_ROOT +file_name,"wb")
				filee.write(data)
				# print stru + "deleted from folder"
				filee.close()
				if curr_image!="avatar.png":
					os.unlink(conf_settings.IMAGE_ROOT + curr_image)
				Registered_Employee_Detail.objects.filter(emp_email=emp_email).update(emp_first_name=emp_first_name,emp_last_name=emp_last_name,emp_full_name=emp_full_name,emp_email=emp_email,emp_password=emp_password,emp_address=emp_address,emp_gender=emp_gender,emp_marital_status=emp_marital_status,emp_contact_number=emp_contact_number,emp_role=emp_role,emp_profile_pic=file_name)


			Registered_Employee_Detail.objects.filter(emp_email=emp_email).update(emp_first_name=emp_first_name,emp_last_name=emp_last_name,emp_full_name=emp_full_name,emp_email=emp_email,emp_password=emp_password,emp_address=emp_address,emp_gender=emp_gender,emp_marital_status=emp_marital_status,emp_contact_number=emp_contact_number,emp_role=emp_role,emp_profile_pic=file_name)
			content['success_upadate_message']="Data Updated successfully"
			return fetch_users_for_admin(request)

		# return render_to_response("Admin/generatelist.html",content,context_instance=RequestContext(request))
	return render_to_response("Admin/index.html",content,context_instance=RequestContext(request))
	

@user_login_required
def del_user_by_admin(request):
	content={}
	session=request.session['user_session']
	content.update(csrf(request))
	if request.method=="GET":
		ids=request.GET['id']
		details=Registered_Employee_Detail.objects.filter(emp_id=ids)
		# content['firstname']=details[0].emp_first_name
		# content['lastname']=details[0].emp_last_name
		# content['email']=details[0].emp_email
		# content['password']=details[0].emp_password
		# content['address']=details[0].emp_address
		# content['gender']=details[0].emp_gender
		# content['marry']=details[0].emp_marital_status
		# content['phone']=details[0].emp_contact_number
		# content['role']=details[0].emp_role
		details.delete()
		return fetch_users_for_admin(request)

	return render_to_response("Admin/delete_user.html",content,context_instance=RequestContext(request))


# def delete_user(request):
# 	content={}
# 	session=request.session['user_session']
# 	content.update(csrf(request))
# 	if request.method=="GET":
# 		email=request.GET['id']
# 		details=Registered_Employee_Detail.objects.filter(emp_email=email)
# 		print details

# 	return render_to_response("index.html")


# def upload(request):
# 	content={}
# 	content.update(csrf(request))
# 	if request.method=="POST":
# 		filee=request.FILES['image']

# 		#f = open(settings.IMAGE_ROOT,"ListingImages\\Customer-%s.%s" %(cid,flist[1]), "wb")
# 		file_name = filee.name
# 		flist = file_name.split(".")
# 		data = filee.read()
# 		filee.close()
# 		filee = open(conf_settings.IMAGE_ROOT +"file_name"+str(randint(2,1000)),"wb")
		
# 		filee.write(data)
# 		filee.close()


# 		# imageUrl  = "%s.%s" %(memberedit.member_uid,flist[1])

# 	return render_to_response("image_upload.html",content,context_instance=RequestContext(request))

def policy(request):
	return render_to_response("policy.html")


def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(10,820,"Hello world how is the day")

   
    p.save()
    return response


@user_login_required
def generate_id(request):
	content={}

	session=request.session['user_session']
	content.update(csrf(request))
	current_user_detail=Registered_Employee_Detail.objects.filter(emp_email=session)

	content['profile_pic1']=current_user_detail[0].emp_profile_pic
	content['firstname1']=current_user_detail[0].emp_first_name
	if request.method=="GET":
		details=Registered_Employee_Detail.objects.filter(emp_email=session)
		content['firstname']=details[0].emp_first_name
		content['lastname']=details[0].emp_last_name
		content['email']=details[0].emp_email
		content['password']=details[0].emp_password
		content['address']=details[0].emp_address
		content['gender']=details[0].emp_gender
		content['marry']=details[0].emp_marital_status
		content['phone']=details[0].emp_contact_number
		content['role']=details[0].emp_role
		content['profile_pic']=details[0].emp_profile_pic
		content['emp_id']=details[0].emp_id
		if details[0].emp_role.lower()=="admin":
			return render_to_response("Admin/generate_id.html",content,context_instance=RequestContext(request))
		else:
			return render_to_response("users/generate_id.html",content,context_instance=RequestContext(request))
	elif request.method=="POST":
		a=Registered_Employee_Detail.objects.filter(emp_email=session)
		a[0].emp_id
		filename=a[0].emp_id+"_"+a[0].emp_first_name+".pdf"

		
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename= %s' %(filename)
		
		card=canvas.Canvas(response)
		card.drawInlineImage(conf_settings.IMAGE_ROOT+"12.png", 0, 0, width=225, height=135)
		# logo image for pdf
		card.drawImage(conf_settings.IMAGE_ROOT+"a.png",10,110,width=20, height=20)
		card.setFont("Helvetica", 14)
		card.setFillColor(HexColor(0x0000ff))
		card.drawString(50,118,"EMPLOYEE WORLD")
		card.setStrokeColorRGB(225,255,1)
		card.line(0,105,225,105)
		# card image for pdf
		card.drawImage(conf_settings.IMAGE_ROOT+a[0].emp_profile_pic,13,50,width=30, height=35)
		card.setFont("Helvetica", 10)
		card.setFillColor(HexColor(0x000000))
		card.drawString(57,75,"Name")
		card.drawString(110,75,a[0].emp_first_name+" "+a[0].emp_last_name )
		card.drawString(57,60,"Gender")
		card.drawString(110,60,a[0].emp_gender)
		card.drawString(57,45,"Email")
		card.drawString(110,45,a[0].emp_email )
		card.drawString(57,30,"Contact")
		card.drawString(110,30,str(a[0].emp_contact_number))
		# data=[["name",a[0].emp_first_name+" "+a[0].emp_last_name],
		# ["Gender",a[0].emp_gender],["Email",a[0].emp_email ],["Contact",str(a[0].emp_contact_number)]]
		# tab=Table(data)

		card.line(0,15,225,15)

		card.setPageSize((225,135))
		card.save()
		return response


	return render_to_response("users/generate_id.html")

@user_login_required
def edit_image(request):
	content={}

	session=request.session['user_session']
	content.update(csrf(request))
	current_user_detail=Registered_Employee_Detail.objects.filter(emp_email=session)

	content['profile_pic1']=current_user_detail[0].emp_profile_pic
	content['firstname1']=current_user_detail[0].emp_first_name
	
	detailss=Registered_Employee_Detail.objects.filter(emp_email=session)
	curr_image=detailss[0].emp_profile_pic
	if request.method=="GET":
		ids=request.GET['id']
		request.session['tempid']=ids
	elif request.method=="POST":
		
		print request.session['tempid']
		pic=request.FILES['profile_pic']
		print pic
		
		file_name = str(randint(2,1000)) + pic.name
		data = pic.read()
		pic.close()
		picc = open(conf_settings.IMAGE_ROOT +file_name,"wb")
		picc.write(data)
		picc.close()

		
		Registered_Employee_Detail.objects.filter(emp_id=request.session['tempid']).update(emp_profile_pic=file_name)
		# os.unlink(conf_settings.IMAGE_ROOT + curr_image)
		del request.session['tempid']
	
	# details=Registered_Employee_Detail.objects.filter(emp_email=session).update(emp_profile_pic=pic)
	return render_to_response("edit_image.html",content,context_instance=RequestContext(request))

def remove_profile_pic(request):
	content={}

	session=request.session['user_session']
	content.update(csrf(request))
	detail=Registered_Employee_Detail.objects.filter(emp_email=session)
	curr_image=detail[0].emp_profile_pic
	Registered_Employee_Detail.objects.filter(emp_email=session).update(emp_profile_pic="avatar.png")
	if curr_image!="avatar.png":
		os.unlink(conf_settings.IMAGE_ROOT+curr_image)
	return HttpResponseRedirect("edit_user")

def handler404(request):
	content={}
	return render_to_response("404.html",content,context_instance=RequestContext(request))

def handler500(request):
	content={}
	return render_to_response("500.html",content,context_instance=RequestContext(request))


#@@@@@@@@@@@@@@ Dashboard coding from here to end of this comment @@@@@@@@@@@@@
