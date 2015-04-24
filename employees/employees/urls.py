from django.conf.urls import patterns, include, url
from django.contrib import admin

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
    # url(r'^index',"admin_activity_page"),

)
