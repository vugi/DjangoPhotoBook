from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView, CreateView, DeleteView, DetailView, ListView, UpdateView
from django.contrib.auth.decorators import login_required

from models import *
from views import *

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

urlpatterns = patterns('',
    url(r'^$', Index.as_view(), name='index'),
    #albums list
    url(r'^album/$', ListView.as_view(model = Album, template_name = 'photobook/album_list.html'), name='album_list_view'),
    #album view
    url(r'^album/(?P<pk>\d+)/$', AlbumDetailView.as_view(model=Album, template_name='photobook/album_detail.html'), name='album_detail_view'), 
    #edit album
    url(r'^album/(?P<pk>\d+)/edit/$', AlbumDetailView.as_view(model=Album, template_name='photobook/album_edit.html'), name='edit_book_view'),
    #new album
    url(r'^album/create/$', login_required(create_album), name='create_album_view'),
	#page view
    url(r'^album/(?P<album>\d+)/(?P<page_number>\d+)/$', page_detail, name='page_detail_view'),   
	#login view
	url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
	#logout view
	url(r'^logout/$', logout_view, name="logout"),
	#register view
	url(r'^register/$', register, name="register"),
    #user list
    url(r'^user/$', login_required(ListView.as_view(model = User, template_name = 'photobook/user_list.html')), name='user_list_view'),
    #user detail view
    url(r'^users/(?P<user_name>\S+)/$', user_detail_view, name="user_detail_view"),
    #json get page information
    url(r'^album/(?P<album_id>\d+)/(?P<page_number>\d+)/json/$', get_or_save_page, name='get_or_save_page'),
    #delete album
    url(r'^album/(?P<album_id>\d+)/delete/$', delete_album, name="delete_album"),
    #delete page
    url(r'^album/(?P<album>\d+)/(?P<page_number>\d+)/delete/$', delete_page, name='delete_page'),
)
