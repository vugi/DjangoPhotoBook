# Create your views here.
from django.conf import settings
from django.views.generic import View, CreateView, DeleteView, DetailView, TemplateView, UpdateView, ListView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

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

    template_name = 'photobook/album_detail.html'
    model = Album
    context_object_name = "album"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the pages
        context['page_list'] = Page.objects.all()
        #context['page_list'] = Page.objects.filter(album=self)
        return context