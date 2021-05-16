from django.urls import path, re_path, include
from django.views.static import serve

from chat_socket import views
from . import settings

from django.conf.urls import url


urlpatterns = [
    path('chat/', views.index),
    url('conn', views.conn),
    path('user/', include('users.urls')),
    path('save/', views.save),
]

if not settings.DEBUG:
    from settings import STATIC_ROOT
    urlpatterns.append(re_path('static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}))
