from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView, CreateView, DeleteView, DetailView, ListView, UpdateView
#from django.contrib.auth.models import User
#from django.contrib.auth.decorators import login_required

from models import *
from views import *

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name = 'photobook/index.html'), name='index'),
    #albums list
    url(r'^album/$', ListView.as_view(model = Album, template_name = 'photobook/album_list.html'), name='album_list_view'),
    #album view
    url(r'^album/(?P<pk>\d+)/$', AlbumDetailView.as_view(model=Album, template_name='photobook/album_detail.html'), name='album_detail_view'),
    #page view
    url(r'^album/(?P<album>\d+)/(?P<page_number>\d+)/$', page_detail, name='page_detail_view'),    
    #edit album
 #   url(r'^album/(?P<pk>\d+)/edit/$', UpdateView.as_view(model=Album, template_name='photobook/album_edit.html'), name='edit_book_view'),
    #new album
 #   url(r'^album/create/$', create_album, name='create_album_view'),
)