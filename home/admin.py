from django.contrib import admin
from django.utils.html import format_html
from .models import Colab, PHD, PostDoc, Project, Alumni, News, Publication, Gallery
# Register your models here.
#admin.site.register(Colab)
#admin.site.register(PHD)
#admin.site.register(PostDoc)
#admin.site.register(Project)
#admin.site.register(Alumni)
admin.site.register(Publication)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "content")


class PHDAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    list_display = ['name','image_tag',]


admin.site.register(PHD, PHDAdmin)
admin.site.register(PostDoc, PHDAdmin)
admin.site.register(Project, PHDAdmin)
admin.site.register(Alumni, PHDAdmin)
admin.site.register(Colab, PHDAdmin)
class PhotoAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    list_display = ['short_desc','image_tag',]
admin.site.register(Gallery, PhotoAdmin)