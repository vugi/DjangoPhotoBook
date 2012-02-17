from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Font(models.Model):
    '''Font used for caption'''
    size = models.PositiveIntegerField()  
    family = models.CharField(max_length=255)
    color = models.CharField(max_length=7) #Hex Color, e.g. "#FF0000"
    
    def __unicode__(self):
        return self.family
    
class Caption(models.Model):
    '''Caption on a page'''
    content = models.TextField()
    font = models.ForeignKey(Font)
    #position = models.ForeignKey(Position)
    
    def __unicode__(self):
        return self.content
    
class Image(models.Model):
    '''Image on a page'''
    url = models.CharField(max_length=1024)
    #position = models.ForeignKey(Position)
    
    def __unicode__(self):
        return self.url

    #def natural_key(self):
    #    return (self.url, self.position.natural_key())
    #natural_key.dependencies = ['photobook.position']

class Position(models.Model):
    '''Position of a layout element'''
    x = models.IntegerField() #default values?
    y = models.IntegerField() 
    z = models.IntegerField(default=0) 
    h = models.PositiveIntegerField() 
    w = models.PositiveIntegerField() 
    image = models.ForeignKey(Image, blank=True, null=True)
    caption = models.ForeignKey(Caption, blank=True, null=True)
    
    def __unicode__(self):
        return '%s, %s, %s, %s, %s' % (self.x, self.y, self.z, self.h, self.w)
    
    #def natural_key(self):
    #    return (self.x, self.y, self.z, self.h, self.w)
    
        
class Layout(models.Model):
    '''Layout of a page'''
    position = models.ManyToManyField(Position)
    
    #def __unicode__(self):
    #    return self.
    
class Album(models.Model):
    '''Photo album'''
    class Meta:
        ordering = ['-pub_date']
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    pub_date = models.DateField()
    height = models.PositiveIntegerField() #px or cm?
    width = models.PositiveIntegerField() #px or cm?
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/album/%i/' % (self.id)
    
class Page(models.Model):
    '''Single page of an album'''
    class Meta:
        ordering = ['number']
        unique_together = ("album", "number")
        
    album = models.ForeignKey(Album) 
    #layout = models.ForeignKey(Layout)
    #images = models.ManyToManyField(Image, blank=True, null=True)
    #captions = models.ManyToManyField(Caption, blank=True, null=True)
    positions = models.ManyToManyField(Position, blank=True, null=True)
    number = models.PositiveIntegerField()
    
    def __unicode__(self):
        return '%s, %s' % (self.album, self.number)
    
    def get_absolute_url(self):
        return '/album/%i/%i/' % (self.album.id, self.number)