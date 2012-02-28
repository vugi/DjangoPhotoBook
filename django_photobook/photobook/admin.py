""" django autoadmin (/admin) """
from photobook.models import *
from django.contrib import admin

admin.site.register(Album)
admin.site.register(Page)
admin.site.register(Layout)
admin.site.register(Position)
admin.site.register(Caption)
admin.site.register(Image)