# Create your views here.
from django.conf import settings
from django import forms
from django.views.generic import View, CreateView, DeleteView, DetailView, TemplateView, UpdateView, ListView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.core import serializers
from django.core.exceptions import ValidationError

import json

# Photobook project imports
from photobook.models import *

class Index(TemplateView):
    template_name = 'photobook/index.html'
	
# Detail view for Albums
class AlbumListView(ListView):
    model = Album
    template_name = 'photobook/album_list.html'
    context_object_name = "album_list"
    
# Detail view for Albums
class AlbumDetailView(DetailView):
    context_object_name = "album"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the pages of the album
        context['page_list'] = Page.objects.filter(album=self.object.id)
        return context

'''Single page view, change to return JSON'''
def page_detail(request, album, page_number):
    album_pages = Page.objects.filter(album__id=album)
    page = album_pages.get(number=page_number)    
    return render_to_response('photobook/page_detail.html', {'page': page}, context_instance=RequestContext(request))
#List view for users
class UserListView(ListView):
    model = User
    template_name = 'photobook/user_list.html'
    context_object_name = "user_list"
    
# Register view
def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/album/")
        else:
            return render_to_response("registration/register.html", {
                'form' : form
            }, context_instance=RequestContext(request))
    else:
        form = UserCreationForm()

    return render_to_response("registration/register.html", {
        'form' : form
    }, context_instance=RequestContext(request))
    
def user_view(request, user_name):
    if (request.user.is_authenticated() and request.user.username == user_name):
        str = "You are looking at your own page"
    else:
        str = "You are looking at someone else's page"
    userName = request.user.username
    return render_to_response('photobook/user_detail.html', {'user' : request.user, 'str' : str, 'owner' : user_name }, context_instance=RequestContext(request))

def json_get_page(request, album_id, page_id):
    album_pages = Page.objects.filter(album__id=album_id)
    page = album_pages.filter(number=page_id) 
    data = serializers.serialize('json', page, use_natural_keys=True)
    return HttpResponse(data, content_type='application/json')

def json_save_page(request):
    if request.is_ajax():
        if request.method == 'POST':
            #data = 'Raw Data: "%s"' % request.raw_post_data 
            '''validation not working'''
            try:
                for obj in serializers.deserialize("json", request.raw_post_data):
                    try:
                        obj.object.full_clean()
                    except ValidationError, e:
                        return HttpResponse(json.dumps({'success': False, 'message': e.message_dict}), content_type='application/json')
                    obj.save()
            except ValidationError, e:
                return HttpResponse(json.dumps({'success': False, 'message': e.messages}), content_type='application/json')    
    return HttpResponse(json.dumps({'success': True, 'message': 'OK'}), content_type='application/json')

    
