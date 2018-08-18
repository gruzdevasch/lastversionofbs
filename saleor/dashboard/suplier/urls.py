from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'suplier/$', views.suplier_list, name='suplier-list'),
    url(r'suplier/add/$', views.suplier_add, name='suplier-add'),
    url(r'suplier/(?P<pk>[0-9]+)/$', views.suplier_edit, name='suplier-update'),
    url(r'suplier/(?P<pk>[0-9]+)/delete/$', views.suplier_delete,
        name='suplier-delete')
    ]
