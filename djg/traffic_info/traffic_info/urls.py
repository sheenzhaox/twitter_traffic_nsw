from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'traffic_info.views.home', name='home'),
    # url(r'^traffic_info/', include('traffic_info.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    # ``r'' is a literal prefix. The content string after ``r'' prefix will do 
    # no format translation. For example: r'\n' means two-character string 
    # \ and n; '\n' represents new line. 
    
    
    url(r'^hello/$', views.hello),  # ^ means start from hello SHARP
                                    # $ means end with hello SHARP
                                    
    url(r'^traffictext/$', views.traffic_text),
)
