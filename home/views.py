import os
import pandas as pd
from django.conf import settings  # type: ignore
from django.core.mail import send_mail  # type: ignore
from django.http import HttpResponse, HttpResponseRedirect  # type: ignore
from django.shortcuts import reverse  # type: ignore
from django.shortcuts import redirect, render  # type: ignore
from django.template.loader import render_to_string # type: ignore

from .forms import ContactForm
from .models import PHD, Alumni, Colab, Gallery, News, PostDoc, Project, Publication, Research, Publication_Research

sync = False


def error_404(request, exception):
    return render(request, "home/404.html", status=404)


def home(request):
    query = Colab.objects.all()
    news = News.objects.all()
    result = ""
    form = ""
    # if request.method == "POST":
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         send_mail(
    #             form.cleaned_data["subject"],  # subject
    #             f"Via website : Message from {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
    #             f"{form.cleaned_data['message']}",  # message
    #             {form.cleaned_data["email"]},  # from email
    #             ["dibyendumaity1999@bose.res.in"],  # replace with your email
    #         )
    #         result = "Your message has been sent!"
    #         return HttpResponseRedirect(reverse("home"))
    # else:
    #     form = ContactForm()

    research = Research.objects.all()
    pr = Publication_Research.objects.all()
    list_result = [entry for entry in pr.values()]
    df = pd.DataFrame(list_result)
    df.groupby('research_id').apply(lambda x: x['link'].tolist(), include_groups=False)
    for i in range(len(research)):
        research[i].publication = df[df['research_id'] == research[i].id]['link'].tolist()

    text = render(
        request,
        "home/home.html",
        {"object": query, "news": news, "form": form, "result": result, "research": research},
    )
    if sync:
        with open("index.html", "wb") as f:
            f.write(text.content)
    return text


def team(request):
    phd = PHD.objects.all()
    postdoc = PostDoc.objects.all()
    project = Project.objects.all()
    alumni = Alumni.objects.all()

    text = render(
        request,
        "home/team.html",
        {"phd": phd, "postdoc": postdoc, "project": project, "alumni": alumni},
    )
    if sync:
        with open("team.html", "wb") as f:
            f.write(text.content)
    return text


def contacts(request):
    result = ""
    form = ""
    # if request.method == "POST":
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         return formated_mail(form)
    # else:
    #     form = ContactForm()
    text = render(request, "home/contact.html", {"form": form, "result": result})
    if sync:
        with open("contacts.html", "wb") as f:
            f.write(text.content)
    return text


# TODO Rename this here and in `contacts`
def formated_mail(form):
    subject = (form.cleaned_data["subject"],)
    from_name = form.cleaned_data["name"]
    from_email = form.cleaned_data["email"]
    message = form.cleaned_data["message"]
    html_content = render_to_string(
        "home/email.html",
        context={
            "name": from_name,
            "email": from_email,
            "message": message,
            "subject": subject,
        },
    )

    send_mail(
        form.cleaned_data["subject"],  # subject
        f"Message from {form.cleaned_data['name']} <{form.cleaned_data['email']}>\n\n"
        f"{form.cleaned_data['message']}",  # message
        None,  # from email
        ["dibyendumaity1999@bose.res.in"],  # replace with your email
        html_message=html_content,
    )
    result = "Your message has been sent!"
    return HttpResponseRedirect(reverse("home"))


def research2(request):
    text = render(request, "home/research.html")
    if sync:
        with open("research.html", "wb") as f:
            f.write(text.content)
    return text

def research(request):
    research = Research.objects.all()
    pr = Publication_Research.objects.all()
    list_result = [entry for entry in pr.values()]
    df = pd.DataFrame(list_result)
    df.groupby('research_id').apply(lambda x: x['link'].tolist(), include_groups=False)
    for i in range(len(research)):
        research[i].publication = df[df['research_id'] == research[i].id]['link'].tolist()
    text = render(request,  "home/research.html", {"research": research})
    text = render(request,  "home/research2.html", {"research": research})
    return text

def news(request):
    news = News.objects.all().order_by("-date")
    text = render(request, "home/news.html", {"news": news})
    if sync:
        with open("news.html", "wb") as f:
            f.write(text.content)
    return text


def publication(request):
    #publication = Publication.objects.all()
    publication = Publication.objects.all().order_by('created_at').reverse()
    text = render(request, "home/publication.html", {"publication": publication})
    if sync:
        with open("publication.html", "wb") as f:
            f.write(text.content)
    return text


def gallery(request):
    gallery = Gallery.objects.all().order_by("-date")
    text = render(request, "home/gallery.html", {"gallery": gallery})
    if sync:
        with open("gallery.html", "wb") as f:
            f.write(text.content)
    return text


def softwares(request):
    text = render(request, "home/softwares.html")
    if sync:
        with open("softwares.html", "wb") as f:
            f.write(text.content)
    return text


def positions(request):
    text = render(request, "home/position.html")
    if sync:
        with open("positions.html", "wb") as f:
            f.write(text.content)
    return text
