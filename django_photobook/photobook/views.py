# Create your views here.
from django.conf import settings
from django import forms
from django.views.generic import View, CreateView, DeleteView, DetailView, TemplateView, UpdateView, ListView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext

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