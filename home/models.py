import datetime
from django.core.validators import MaxValueValidator, MinValueValidator # type: ignore
from django.db import models # type: ignore

# Create your models here.

class Colab(models.Model):
    name = models.TextField(max_length=100)
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100)
    desig = models.TextField()
    univ = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.name
    
class PHD(models.Model):
    name = models.TextField(max_length=100)
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100)
    desig = models.TextField()
    interest = models.TextField()
    subject = models.TextField()
    mail = models.EmailField()
    github = models.URLField()
    twitter = models.URLField()
    linkedin = models.URLField()

    def __str__(self):
        return self.name
    
class PostDoc(models.Model):
    name = models.TextField(max_length=100)
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100)
    degree = models.TextField()
    interest = models.TextField()
    subject = models.TextField()
    mail = models.EmailField()
    github = models.URLField()
    twitter = models.URLField()
    linkedin = models.URLField()

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.TextField(max_length=100)
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100)
    desig = models.TextField()
    interest = models.TextField()
    subject = models.TextField()
    mail = models.EmailField()
    github = models.URLField()
    twitter = models.URLField()
    linkedin = models.URLField()

    def __str__(self):
        return self.name

class Alumni(models.Model):
    name = models.TextField(max_length=100)
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100)
    desig = models.TextField()
    role = models.TextField()
    subject = models.TextField()
    mail = models.EmailField()


    def __str__(self):
        return self.name
    
class News(models.Model):
    title = models.TextField(max_length=100)
    date = models.DateField()
    content = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Publication(models.Model):
    title = models.TextField(max_length=100)
    year = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(2005), max_value_current_year])
    authors = models.CharField(max_length=200)
    journal = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.title
    
class Gallery(models.Model):
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=100)
    short_desc = models.TextField(max_length=100)
    long_desc =  models.TextField(max_length=400)
    date = models.DateField()

    def __str__(self):
        return self.short_desc