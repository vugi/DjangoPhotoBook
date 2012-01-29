from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView, CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib.auth.decorators import login_required

from models import *
from views import *

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    #albums list
    url(r'^album/$', login_required(ListView.as_view(model = Album, template_name = 'photobook/album_list.html')), name='album_list_view'),
    #album view
    url(r'^album/(?P<pk>\d+)/$', AlbumDetailView.as_view(model=Album, template_name='photobook/album_detail.html'), name='album_detail_view'),
    #page view
    url(r'^album/(?P<album>\d+)/(?P<page_number>\d+)/$', page_detail, name='page_detail_view'),    
    #edit album
 #   url(r'^album/(?P<pk>\d+)/edit/$', UpdateView.as_view(model=Album, template_name='photobook/album_edit.html'), name='edit_book_view'),
    #new album
 #   url(r'^album/create/$', create_album, name='create_album_view'),
	#login view
	url(r'^login/$', 'django.contrib.auth.views.login'),
	#logout view
	url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
	#register view
	url(r'^register/$', register, name="register"),
	
)