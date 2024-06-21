from django.contrib import admin
from .models import Mebel

class MebelAdmin(admin.ModelAdmin):
    list_display = ['price', 'description', 'parse_datetime', 'link']
    list_display_links = ['description']
    search_fields = ['description']
    # list_editable = ['description']
    list_filter = ['parse_datetime', 'price']

admin.site.register(Mebel, MebelAdmin)
