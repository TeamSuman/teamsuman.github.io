from django.http import HttpResponse, HttpResponseRedirect # type: ignore
from django.core.mail import send_mail # type: ignore
from django.shortcuts import reverse # type: ignore

from django.conf import settings # type: ignore
from django.shortcuts import redirect, render  # type: ignore
from .models import Colab, PHD, PostDoc, Project, Alumni, News, Publication, Gallery
from .forms import ContactForm

def home(request):
    query = Colab.objects.all()
    news = News.objects.all()
    result = ""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data['subject'],  # subject
                f"Via website : Message from {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
                f"{form.cleaned_data['message']}",  # message
                {form.cleaned_data['email']},  # from email
                ['dibyendumaity1999@gmail.com'],  # replace with your email
            )
            result = "Your message has been sent!"
            return HttpResponseRedirect(reverse("home"))
    else:
        form = ContactForm()
    return render(request, "home/home.html", {'object':query, 'news':news, 'form': form, 'result': result})


def team(request):
    phd = PHD.objects.all()
    postdoc = PostDoc.objects.all()
    project = Project.objects.all()
    alumni = Alumni.objects.all()
    
    return render(request, "home/team.html", {'phd':phd, 'postdoc':postdoc,
                                              'project':project, 'alumni':alumni})



def contacts(request):
    result = ""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data['subject'],  # subject
                f"Message from {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
                f"{form.cleaned_data['message']}",  # message
                None,  # from email
                ['dibyendumaity1999@gmail.com'],  # replace with your email
            )
            result = "Your message has been sent!"
            return HttpResponseRedirect(reverse("home"))
    else:
        form = ContactForm()
    return render(request, "home/contact.html", {'form': form, 'result': result})

def research(request):
    return render(request, "home/research.html")

def news(request):
    news = News.objects.all().order_by('-date')
    return render(request, "home/news.html", {'news':news})


def publication(request):
    publication = Publication.objects.all()
    return render(request, "home/publication.html", {'publication':publication})

def gallery(request):
    gallery = Gallery.objects.all().order_by('-date')
    return render(request, "home/gallery.html", {'gallery':gallery})

def softwares(request):
    return render(request, "home/softwares.html")


def positions(request):
    return render(request, "home/position.html")