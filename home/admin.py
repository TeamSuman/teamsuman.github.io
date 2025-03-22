from django.contrib import admin # type: ignore
from django.utils.html import format_html # type: ignore
from .models import Colab, PHD, PostDoc, Project, Alumni, News, Publication, Gallery, Research, Publication_Research
# Register your models here.
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

@admin.register(Publication_Research)
class PubResModelAdmin(admin.ModelAdmin):
  fields = ('link', 'research')

from django.contrib.admin.options import TabularInline

class PubResAdminInline(TabularInline):
    extra = 1
    model = Publication_Research

class ResearchAdmin(admin.ModelAdmin):
    inlines = (PubResAdminInline,)
    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

    list_display = ['title','image_tag',]

admin.site.register(Research, ResearchAdmin)



