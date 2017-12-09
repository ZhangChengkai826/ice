from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='main_app_index'),
    url(r'^diary$', views.diary, name='main_app_diary'),
    url(r'^photo$', views.photo, name='main_app_photo'),
]