from django.conf.urls import url

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'analyser'
urlpatterns = [
    url(r'^analyse', views.analyse, name='analyse'),
    url(r'^', views.index, name='index'),
]
