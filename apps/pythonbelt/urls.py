from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process', views.process),
    url(r'^login', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^additem', views.additem),
    url(r'^wish_items/create$', views.createItem),
    url(r'^addNew', views.addNew),
    url(r'^item/(?P<id>\d+)$', views.item),
    url(r'^item/remove/(?P<id>\d+)$', views.remove),
    url(r'^delete', views.delete),
    url(r'^logout$', views.logout)
]
