from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^senica/$', views.senica, name='senica'),
    url(r'^senica/(?P<room_number>\d+)/$', views.senica_room_filter, name='senica_room_filter'),
]