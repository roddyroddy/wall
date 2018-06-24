from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index), #this is for display
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'logoff$', views.logoff),
    url(r'success$' , views.success),
    url(r'newmessage$', views.newmessage),
    url(r'comment$', views.newcomment), 
    url(r'delete$', views.deletemessage),
    url(r'deletem$', views.deletecomment)
]                            
