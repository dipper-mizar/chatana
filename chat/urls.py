from django.urls import path, re_path, include
from django.views.static import serve
from django.views import i18n
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from chat_socket import views
from . import settings


urlpatterns = [
    path('chat/', views.index),
    url('conn', views.conn),
    path('user/', include('users.urls')),
    path('save/', views.save),
    path('load_records/', views.load_record)
]

if not settings.DEBUG:
    urlpatterns.append(re_path('static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}))
    urlpatterns += staticfiles_urlpatterns()

urlpatterns.append(path('jsi18n/users', i18n.JavaScriptCatalog.as_view(packages=['users']), name='jsi18n'))
urlpatterns.append(path('i18n/', include('django.conf.urls.i18n')))
