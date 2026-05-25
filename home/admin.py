from django.contrib import admin
from django.contrib.admin.options import TabularInline
from django.utils.html import format_html
from django.utils.text import Truncator

try:
    from adminsortable2.admin import SortableAdminMixin
except ModuleNotFoundError:
    class SortableAdminMixin:
        pass

from .models import (
    PHD,
    Alumni,
    Colab,
    Gallery,
    News,
    PostDoc,
    Project,
    Publication,
    Publication_Research,
    Research,
    SoftwareProject,
    Animation,
    Poster,
    ProjectAlumni,
    TeamPage,
    HomePageConfiguration,
    HeroSlide,
)


# -----------------------------
# Simple Model Registrations
# -----------------------------
admin.site.register(Publication)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Admin for News with title and content visible in list view."""
    list_display = ("title", "content")


# -----------------------------
# Shared Admin Utilities
# -----------------------------
class ImageAdminMixin:
    """Mixin to display image thumbnails in list_display."""

    def image_tag(self, obj):
        if getattr(obj, "image", None):
            return format_html(
                '<img src="{}" style="max-width:200px; max-height:200px"/>', obj.image.url
            )
        return ""

    image_tag.short_description = "Image"


class ShortDescriptionAdminMixin:
    """Mixin to show truncated description and links in list_display."""

    @admin.display(description="Description")
    def short_description(self, obj):
        return Truncator(getattr(obj, "description", "")).chars(70)

    @admin.display(description="Publication")
    def publication_link(self, obj):
        url = getattr(obj, "publication_url", None)
        if url:
            return format_html('<a href="{}" target="_blank">View Paper</a>', url)
        return "—"

    @admin.display(description="Repository")
    def repo_link(self, obj):
        url = getattr(obj, "repo_url", None)
        if url:
            return format_html('<a href="{}" target="_blank">View Code</a>', url)
        return "—"


# -----------------------------
# Software Projects Admin
# -----------------------------
@admin.register(SoftwareProject)
class SoftwareAdmin(SortableAdminMixin, ShortDescriptionAdminMixin, admin.ModelAdmin):
    """Admin for SoftwareProject with sortable ordering and link previews."""

    list_display = (
        "name",
        "short_description",
        "status",
        "publication_link",
        "repo_link",
    )
    list_display_links = ("name",)
    search_fields = ("name", "description", "tags")
    list_filter = ("status",)

    fieldsets = (
        ("Core Information", {"fields": ("name", "description", "tags")}),
        (
            "Links & Status",
            {
                "fields": ("publication_url", "repo_url", "status"),
                "description": "Provide relevant URLs and current project status.",
            },
        ),
    )


# -----------------------------
# People Admin (PHD, PostDoc, Project, Alumni, Colab)
# -----------------------------
class PeopleAdmin(SortableAdminMixin, ImageAdminMixin, admin.ModelAdmin):
    list_display = ("name", "image_tag")


admin.site.register(PHD, PeopleAdmin)
admin.site.register(PostDoc, PeopleAdmin)
admin.site.register(Project, PeopleAdmin)
admin.site.register(Alumni, PeopleAdmin)
admin.site.register(Colab, PeopleAdmin)


# -----------------------------
# Gallery Admin
# -----------------------------
class PhotoAdmin(SortableAdminMixin, ImageAdminMixin, admin.ModelAdmin):
    list_display = ("short_desc", "image_tag")


admin.site.register(Gallery, PhotoAdmin)


# -----------------------------
# Project Alumni Admin
# -----------------------------
@admin.register(ProjectAlumni)
class ProjectAlumniAdmin(SortableAdminMixin, ImageAdminMixin, admin.ModelAdmin):
    list_display = ("name", "project_title", "duration")
    search_fields = ("name", "project_title")


# -----------------------------
# Team Page Settings Admin
# -----------------------------
@admin.register(TeamPage)
class TeamPageAdmin(ImageAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "lab_title", "pi_name")

    def has_add_permission(self, request):
        # Allow adding only if no instance exists

        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


# -----------------------------
# Home Page Configuration Admin
# -----------------------------
@admin.register(HomePageConfiguration)
class HomePageConfigurationAdmin(ImageAdminMixin, admin.ModelAdmin):
    list_display = ("__str__", "about_title", "research_title")

    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(HeroSlide)
class HeroSlideAdmin(SortableAdminMixin, ImageAdminMixin, admin.ModelAdmin):
    list_display = ("caption_title", "image_tag", "is_active", "my_order")
    list_editable = ("is_active", "my_order")
    list_filter = ("is_active",)



# -----------------------------
# Publication Research Admin
# -----------------------------
@admin.register(Publication_Research)
class PubResModelAdmin(admin.ModelAdmin):
    fields = ("link", "research")


class PubResAdminInline(TabularInline):
    model = Publication_Research
    extra = 1


# -----------------------------
# Research Admin
# -----------------------------
@admin.register(Research)
class ResearchAdmin(ImageAdminMixin, admin.ModelAdmin):
    list_display = ("title", "image_tag")

@admin.register(Animation)
class AnimationAdmin(admin.ModelAdmin):
    list_display = ('short_desc', 'date', 'my_order')
    list_editable = ('my_order',)

@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = ('short_desc', 'date', 'my_order')
    list_editable = ('my_order',)
