import datetime

#from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

try:
    from django_ckeditor_5.fields import CKEditor5Field
except ModuleNotFoundError:
    class CKEditor5Field(models.TextField):
        def __init__(self, *args, **kwargs):
            kwargs.pop("config_name", None)
            super().__init__(*args, **kwargs)


# -----------------------------
# Helper Functions
# -----------------------------
def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


# -----------------------------
# Base People Model Mixin
# -----------------------------
class PersonMixin(models.Model):
    """Mixin for common person fields."""
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")
    mail = models.EmailField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["my_order"]

    def __str__(self):
        return self.name


# -----------------------------
# Collaborators / Team Members
# -----------------------------
class Colab(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")
    desig = models.CharField(max_length=100)
    univ = models.CharField(max_length=100)
    link = models.URLField()
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["my_order"]

    def __str__(self):
        return self.name


class PHD(PersonMixin):
    desig = models.CharField(max_length=100)
    interest = models.TextField()
    subject = models.TextField()


class PostDoc(PersonMixin):
    degree = models.CharField(max_length=100)
    interest = models.TextField()
    subject = models.TextField()


class Project(PersonMixin):
    desig = models.CharField(max_length=100)
    interest = models.TextField()
    subject = models.TextField()


class Alumni(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")
    desig = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    mail = models.EmailField(null=True, blank=True)
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["my_order"]
        verbose_name_plural = "Alumni"

    def __str__(self):
        return self.name



# -----------------------------
# Project Alumni
# -----------------------------
class ProjectAlumni(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=100, help_text="e.g. 'Summer 2023' or '2023-2024'")
    project_title = models.CharField(max_length=200)
    current_position = models.CharField(max_length=200, blank=True)
    email = models.EmailField(null=True, blank=True)
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["my_order"]
        verbose_name_plural = "Project Alumni"

    def __str__(self):
        return self.name



# -----------------------------
# Team Page Configuration
# -----------------------------
class TeamPage(models.Model):
    # Lab Group Section
    lab_title = models.CharField(max_length=200, default="Chakrabarty Lab, 2024")
    group_image = models.ImageField(upload_to="images/", help_text="Upload the main group photo")
    group_caption = models.TextField(help_text="Caption map for the group photo (e.g. '(From left) Name1, Name2...')")

    # PI Section
    pi_name = models.CharField(max_length=100, default="Dr. Suman Chakrabarty")
    pi_role = models.CharField(max_length=100, default="Professor & Group Leader")
    pi_image = models.ImageField(upload_to="images/", help_text="Upload PI's photo")

    pi_department = models.CharField(max_length=200, default="Department of Chemical and Biological Sciences")
    pi_department_url = models.URLField(blank=True, default="https://newweb.bose.res.in/departments/CBS/Faculty.jsp")

    pi_institute = models.CharField(max_length=200, default="S. N. Bose National Centre for Basic Sciences, Kolkata")
    pi_institute_url = models.URLField(blank=True, default="https://newweb.bose.res.in")

    research_interests = models.TextField(help_text="Comma separated list of interests or full text")

    # Social Links
    email = models.EmailField(default="sumanc@bose.res.in")
    google_scholar = models.URLField(blank=True, verbose_name="Google Scholar URL")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn URL")
    twitter = models.URLField(blank=True, verbose_name="Twitter/X URL")
    github = models.URLField(blank=True, verbose_name="GitHub URL")

    class Meta:
        verbose_name = "Team Page Configuration"
        verbose_name_plural = "Team Page Configuration"


    def __str__(self):
        return "Team Page Settings"


# -----------------------------
# Home Page Configuration
# -----------------------------
class HomePageConfiguration(models.Model):
    # About Section
    about_title = models.CharField(max_length=200, default="About Us")
    about_image = models.ImageField(upload_to="images/", help_text="Upload the About Section image")
    about_content = CKEditor5Field("About Content", config_name="extends")

    # Research Section
    research_title = models.CharField(max_length=200, default="Research")
    research_heading = models.CharField(max_length=200, default="Major Research Interests")
    research_description = CKEditor5Field("Research Description", config_name="extends")

    class Meta:
        verbose_name = "Home Page Configuration"
        verbose_name_plural = "Home Page Configuration"

    def __str__(self):
        return "Home Page Configuration"


class HeroSlide(models.Model):
    # For video slides, we can either have a file field or just use the image field.
    # The requirement is flexible, but a separate video field is better.
    # If video is present, it takes precedence.
    image = models.ImageField(upload_to="sliders/", blank=True, null=True, help_text="Background image for the slide")
    video = models.FileField(upload_to="sliders/videos/", blank=True, null=True, help_text="Upload MP4/WebM video (overrides image)")

    caption_title = models.CharField(max_length=200, blank=True, help_text="Main heading in the caption")
    caption_subtitle = models.CharField(max_length=200, blank=True, help_text="Subheading in the caption")

    my_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["my_order"]
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"

    def __str__(self):
        return self.caption_title or f"Slide {self.my_order}"



# -----------------------------
# News
# -----------------------------
class News(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    content = models.TextField()
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["my_order"]
        verbose_name_plural = "News"

    def __str__(self):
        return self.title


# -----------------------------
# Publications
# -----------------------------
class Publication(models.Model):
    title = models.CharField(max_length=1000)
    year = models.PositiveIntegerField(
        default=current_year,
        validators=[MinValueValidator(2005), max_value_current_year],
    )
    authors = models.CharField(max_length=200)
    journal = models.TextField()
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -----------------------------
# Gallery
# -----------------------------
class Gallery(models.Model):
    image = models.ImageField(upload_to="images/")
    short_desc = models.CharField(max_length=100)
    long_desc = models.TextField(max_length=400)
    date = models.DateField()

    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["my_order"]

    def __str__(self):
        return self.short_desc


# -----------------------------
# Research
# -----------------------------
class Research(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/")
    description = models.TextField(max_length=10000)
    content = CKEditor5Field("Text", config_name="extends")
    my_order = models.PositiveIntegerField(default=0)
    selected_publications = models.ManyToManyField(Publication, blank=True, related_name='research_topics')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["my_order"]
        verbose_name_plural = "Research"

class Publication_Research(models.Model):
    link = models.CharField(_("Publications"), max_length=255)
    url = models.URLField(_("Publication URL"), blank=True, null=True, help_text="Optional link to the publication")
    research = models.ForeignKey(Research, verbose_name=_("Link to Research"), on_delete=models.CASCADE)


# -----------------------------
# Software Projects
# -----------------------------
class SoftwareProject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    tags = models.CharField(max_length=200, help_text="Comma-separated tags")
    publication_url = models.URLField(blank=True, null=True)
    repo_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, help_text="e.g., 'In Progress'")
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["my_order"]

    def __str__(self):
        return self.name

    def get_tags_list(self):
        """Return list of tags from comma-separated string."""
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    # Admin display helpers
    def short_description(self):
        return (self.description[:75] + "...") if len(self.description) > 75 else self.description

    def publication_link(self):
        if self.publication_url:
            return format_html('<a href="{}" target="_blank">View</a>', self.publication_url)
        return "—"
    publication_link.short_description = "Publication"

    def repo_link(self):
        if self.repo_url:
            return format_html('<a href="{}" target="_blank">Repo</a>', self.repo_url)
        return "—"
    repo_link.short_description = "Repository"


# New model for Simulations/GIFs/Movies
class Animation(models.Model):
    # Using FileField to allow .mp4 and .mov in addition to .gif
    file = models.FileField(upload_to="animations/")
    short_desc = models.CharField(max_length=100)
    long_desc = models.TextField(max_length=400)
    date = models.DateField()
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["my_order", "-date"]

    def __str__(self):
        return self.short_desc

# New model for Academic Posters
class Poster(models.Model):
    pdf = models.FileField(upload_to="posters/")
    short_desc = models.CharField(max_length=300)
    long_desc = models.TextField(max_length=500)
    date = models.DateField()
    my_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["my_order", "-date"]

    def __str__(self):
        return self.short_desc
