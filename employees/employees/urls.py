from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse

urlpatterns = patterns('employeeapp.views',
    # Examples:
    # url(r'^$', 'employees.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',"login"),
    url(r'^index',"login"),

    url(r'^adduser',"adduser"),
    url(r'^fpass','forgetpassword'),
    url(r'^password_mail',"password_mail"),
    url(r'^logout',"logout"),
    url(r'^reset',"resetpassword"),
    url(r'^verify',"verify"),
    
   
  
    url(r'^admin_index',"admin_index"),
    url(r'^user_index',"user_index"),
    url(r'^ema',"ema"),
    url(r"^generate_list","fetch_users_for_admin"),
    url(r"^edit_user","edit_user_by_admin"),
    url(r"^delete_user","del_user_by_admin"),

    url(r"^generate_id","generate_id"),
    url(r"^gen","some_view"),
    url(r"^edit_image","edit_image"),
    url(r"^remove_pro_image","remove_profile_pic"),
    # url(r'^index',"admin_activity_page"),
    url(r"^fet","facebook_data_fetching_and_authenticating"),
    url(r"^chart","graf"),


)

handler404="employeeapp.views.handler404"
handler500="employeeapp.views.handler500"
