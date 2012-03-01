# Create your views here.
from django.conf import settings
from django import forms
from django.views.generic import View, CreateView, DeleteView, DetailView, TemplateView, UpdateView, ListView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.contrib import messages

from django.core import serializers
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils import simplejson
import json

from forms import *

import flickrapi

# Photobook project imports
from photobook.models import *

class Index(TemplateView):
    template_name = 'photobook/index.html'
	
# List view for Albums
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
        # Check to see if user is owner of the album
        is_owner = False
        album_owner = Album.objects.get(id=self.object.id).user
        if (self.request.user.is_authenticated() and self.request.user.id == album_owner.id):
            is_owner = True
        context['is_owner'] = is_owner
        return context

#Single page view
def page_detail(request, album, page_number):
    album_pages = Page.objects.filter(album__id=album)
    page = album_pages.get(number=page_number)
    is_owner = Album.objects.get(id=album).user.id == request.user.id
    return render_to_response('photobook/page_detail.html', {'page': page, "is_owner": is_owner}, context_instance=RequestContext(request))
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
    is_owner = False;
    if (request.user.is_authenticated() and request.user.username == user_name):
        is_owner = True
    page_owner = User.objects.get(username=user_name)
    album_list = Album.objects.filter(user=page_owner)
    return render_to_response('photobook/user_detail.html', {'page_owner' : page_owner, 'album_list' : album_list, 'is_owner' : is_owner }, context_instance=RequestContext(request))


def get_or_save_page(request, album_id, page_number):
    #if post, save the page and positions
    if request.method == 'POST':
        
        #check that the album exists
        album = None
        try: 
            album = Album.objects.get(id=album_id)
        except Album.DoesNotExist:
            return HttpResponse(json.dumps({'success': False, 'message': 'Album does not exist.'}), status=404, content_type='application/json')    
        
        #check that the logged in user is authorized to make changes 
        logged_user = request.user
        album_owner = Album.objects.get(id=album_id).user
        if (not logged_user.id == album_owner.id):
            return HttpResponse(json.dumps({'success': False, 'message': 'Unauthorized access.'}), status=401, content_type='application/json')    
        
        #if the page does exist, delete all position objects 
        try: 
            page = Page.objects.get(number=page_number, album__id=album_id)
            page.positions.all().delete()
        #else create a new page
        except Page.DoesNotExist:
            page = Page(
                album = Album.objects.get(id=album_id), 
                number = page_number
            )
            try:
                page.full_clean()
            except ValidationError, e:
                return HttpResponse(json.dumps({'success': False, 'message': e.message_dict}), status=404, content_type='application/json')
            page.save()
                    
        #save all positions 
        data = json.loads(request.raw_post_data)
        return add_positions(data, album, page)
        #return HttpResponse(json.dumps({'success': True, 'message': 'OK'}), content_type='application/json')


    #else get page
    
    ''' returns a json in following format:
    {"page": {
        "positions": [
            {
                "caption": null,
                "w": 102,
                "h": 101,
                "y": 1,
                "x": 2,
                "image": "url",
                "z": 1,
                "id": "css style id"
            },
            ...
        ],
    },
    "success": true}
    '''
    try: 
        album = Album.objects.get(id=album_id)
    except Album.DoesNotExist:
        return HttpResponse(json.dumps({'success': False, 'message': 'Album does not exist.'}), status=404, content_type='application/json')    
    try: 
        page = Page.objects.get(number=page_number, album__id=album_id)
    except Page.DoesNotExist:
        return HttpResponse(json.dumps({'success': False, 'message': 'Page does not exist.'}), status=404, content_type='application/json')    
    
    positions = []
    for p in page.positions.all():
        image = None
        if(p.image):
            image = {
                'id' : p.image.id,
                'url': p.image.url
        }
        caption = None
        if(p.caption):
            caption = {
                'id' : p.caption.id,
                'content': p.caption.content,
                'font': p.caption.font
            }
        p = {
             'id': p.id,
             'image': image,
             'caption': caption,
             'x': p.x,
             'y': p.y,
             'z': p.z,
             'h': p.h,
             'w': p.w
        }
        positions.append(p)
    page_information = {
        'album_id': album_id, 
        'page_number': page_number,
        'positions': positions
    }
    return HttpResponse(json.dumps({'success': True, 'page': page_information}), content_type='application/json')


def add_positions(data, album, page):
    '''Adds positions with images and caption to an existing page. 
    Expects json in following format:
    {
        "album_id": 1,
        "page_number": 4,
        "positions": [
            {
               "image": "url",
               "x": "120",
               "y": "120",
               "z": "1",
               "h": "200",
               "w": "202"
            },
            {
               "caption": {
                   "content": string,
                   "font": string /* css style id */ 
               },
               "x": "2",
               "y": "200",
               "z": "1",
               "h": "101",
               "w": "102"
            }
        ],
    }
    '''
    if(not album):
        return HttpResponse(json.dumps({'success': False, 'message': 'Album does not exist.'}), status=404, content_type='application/json')    
    if(not page):
        return HttpResponse(json.dumps({'success': False, 'message': 'Page does not exist.'}), status=404, content_type='application/json')    
    
    #save all positions
    if(data):
        for p in data['positions']:
            image = None
            caption = None
            #save image
            if('image' in p):
                image = Image(url = p['image'])              
                try:
                    image.full_clean()
                except ValidationError, e:
                    return HttpResponse(json.dumps({'success': False, 'message': e.message_dict}), status=404, content_type='application/json')
                image.save()
            #save caption            
            if('caption' in p):
                caption = Caption(content = p['caption']['content'], font = p['caption']['font'])              
                try:
                    caption.full_clean()
                except ValidationError, e:
                    return HttpResponse(json.dumps({'success': False, 'message': e.message_dict}), status=404, content_type='application/json')
                caption.save()
            position = Position(
                x = p['x'], 
                y = p['y'], 
                z = p['z'], 
                h = p['h'], 
                w = p['w'], 
                image = image,
                caption = caption
            )          
            #validate, save and add many to many relationship
            try:
                position.full_clean()
            except ValidationError, e:
                return HttpResponse(json.dumps({'success': False, 'message': e.message_dict}), status=404, content_type='application/json')
            position.save()
            page.positions.add(position)
            
    
    return HttpResponse(json.dumps({'success': True, 'message': 'OK'}), content_type='application/json')

    
    
def search_result(request):
    if request.method == 'POST':
        api_key = 'baeae16ada7e043585db45da91af1601'
        url_base = 'http://farm1.staticflickr.com/'
        flickr = flickrapi.FlickrAPI(api_key)
        photo_urls = []
        form = SearchForm(request.POST)
        if form.is_valid():
            free_text = form.cleaned_data['free_text']
            tags = form.cleaned_data['tags']
            tag_m = form.cleaned_data['tag_mode']
            i = 0
            for p in flickr.walk(tag_mode=tag_m,
                tags=tags,
                text=free_text,
                min_taken_date='2008-08-20',
                max_taken_date='2008-08-21',
                per_page='500'):
                i = i + 1
                if (i > 20):
                    break
                current_url = url_base + p.get('server') + '/' + p.get('id') + '_' + p.get('secret') + '_m.jpg'
                photo_urls.append(current_url)
            return render_to_response('photobook/search_result.html', { 'photo_urls' : photo_urls }, context_instance=RequestContext(request))
        else:
            print 'Form was not valid'
            return HttpResponseRedirect("/album/")
    else:
        return HttpResponseRedirect("/search/")
    
def search(request):
    if request.method == 'GET':
        form = SearchForm()
        return render_to_response('photobook/search.html', { 'form' : form }, context_instance=RequestContext(request))
        
def delete_album(request, album_id):
    logged_user = request.user
    album_owner = Album.objects.get(id=album_id).user
    if (logged_user.id == album_owner.id):
        album = Album.objects.get(id=album_id)
        album.delete()
        return HttpResponseRedirect("/album/")
    else:
        return HttpResponseRedirect("/")

def delete_page(request, album, page_number):
    logged_user = request.user
    album_pages = Page.objects.filter(album__id=album)
    current_page = album_pages.get(number=page_number)
    current_album = Album.objects.get(id=album)
    album_owner = current_album.user
    if (logged_user.id == album_owner.id):
        page_number = current_page.number
        current_page.delete()
        all_pages = current_album.page_set.all()
        for p in all_pages:
            if (p.number > page_number):
                p.number = p.number - 1
                p.save()
        return HttpResponseRedirect("/album/"+str(current_album.id)+"/")
    else:
        return HttpResponseRedirect("/")

@login_required    
def create_album(request):
    if request.method == 'POST':
        form = modelCreationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['album_name']
            height = form.cleaned_data['album_height']
            width = form.cleaned_data['album_width']
            new_album = Album(user = request.user, name = name, height = height, width = width)
            try:
                new_album.full_clean()
                new_album.save()
                return HttpResponseRedirect("/users/" + request.user.username + "/")
            except ValidationError, e:
                print "Failed to validate the model object."
                return HttpResponseRedirect("/")
        else:
            return render_to_response("photobook/create_album.html", {
                'form' : form
            }, context_instance=RequestContext(request))
    else:
        form = modelCreationForm()
        return render_to_response("photobook/create_album.html", {
                'form' : form
            }, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    logged_out = True
    messages.info(request, "Logged out succesfully!")
    return render_to_response("photobook/index.html", { 'logged_out' : logged_out }, context_instance=RequestContext(request))