from django.contrib import admin
from django.utils.html import format_html

from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title_tag', 'description', 'price', 'keep')

    list_editable = ('keep',)

    def image_tag(self, obj):
        return format_html('<img src="{0}" style="width: 120px; height:120px;" />'.format(obj.photo.url))

    def title_tag(self, obj):
        return format_html(f'<a href="{obj.link}" target="_blank">{obj.title}</a>')