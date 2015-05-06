from django.db import models

# Create your models here.
class Registered_Employee_Detail(models.Model):
	gender=(('Male',"Male"),
		("Female","Female"),)

	marital_status=(("Married","Married"),
					("Unmarried","Unmarried")

		)
	role=(
		("Admin","Admin"),
		("User","User")
	)

	emp_id=models.CharField(max_length=10,blank=False,null=False,primary_key=True)
	emp_first_name=models.CharField(max_length=50,null=True)
	emp_last_name=models.CharField(max_length=50)
	emp_full_name=models.CharField(max_length=200)
	emp_email=models.EmailField(blank=False,null=False,unique=True)
	emp_password=models.CharField(max_length=50,blank=False,null=False)
	emp_address=models.TextField(blank=False,null=False)
	emp_gender=models.CharField(max_length=10,blank=False,null=False,choices=gender)
	emp_marital_status=models.CharField(max_length=15,blank=False,null=False,choices=marital_status)
	emp_contact_number=models.IntegerField(max_length=13,blank=False,null=False)
	emp_role=models.CharField(max_length=20,blank=False,null=True,choices=role)
	emp_profile_pic=models.CharField(max_length=200,default="avatar.png")
	is_verified=models.BooleanField(default=False)
	def __str__(self):
		return '%s' %(self.emp_email)




class Department(models.Model):
	emp_id=models.ForeignKey("Registered_Employee_Detail")
	dept_name=models.CharField(max_length=50)
	dept_id=models.CharField(max_length=10)

	def __str__(self):
		return '%s' %(self.dept_name)


class Salary(models.Model):
	emp_id=models.ForeignKey("Registered_Employee_Detail")
	salary=models.FloatField()
	bonus=models.IntegerField(blank=True,null=True)

	def __str__(self):
		return '%s' %(self.salary)


class User_log(models.Model):
	emp_id=models.ForeignKey("Registered_Employee_Detail")
	login_time=models.DateTimeField(auto_now=True)
	logout_time=models.DateTimeField(blank=True)

	def __str__(self):
		return '%s' %(self.logout_time)








