from django.conf.urls import url
from . import views

app_name = 'info'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^activities$', views.activities, name='activities'),


    url(r'^login/$', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),

    url(r'^staff/$', views.staff_index, name='staff_index'),
    url(r'^staff/database_update/$', views.database_update, name='database_update'),
    url(r'^staff/post/$', views.post_board, name='staff_board'),


    url(r'^staff/archive/$', views.archive, name='archive'),
    url(r'^staff/archive/(?P<date>[\w\-]+)/$', views.archive, name='archive'),


    url(r'^staff/super_message/post$', views.super_message_post, name='super_message_post'),
    url(r'^staff/super_message/delete$', views.super_message_delete, name='super_message_delete'),

    url(r'^staff/graph/post$', views.graph_post, name='graph_post'),
    url(r'^staff/graph/delete$', views.graph_delete, name='graph_delete'),

    url(r'^api/$', views.api, name='api'),


    url(r'^createsuperuser/$', views.createsuperuser, name='createsuperuser'),
]
