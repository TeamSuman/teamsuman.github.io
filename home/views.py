# import pandas as pd
from django.core.mail import send_mail  # type: ignore
from django.http import HttpResponseRedirect  # type: ignore
from django.shortcuts import (  # type: ignore
    get_object_or_404,
    render,
    reverse,  # type: ignore
)
from django.template.loader import render_to_string  # type: ignore

from .models import (
    PHD,
    Alumni,
    Colab,
    Gallery,
    Animation,
    Poster,
    News,
    PostDoc,
    Project,
    Publication,
    # Publication_Research,
    Research,
    SoftwareProject,
    ProjectAlumni,
    ProjectAlumni,
    TeamPage,
    HomePageConfiguration,
    HeroSlide,
)

sync = False


def error_404(request, exception):
    return render(request, "home/404.html", status=404)


def home(request):
    query = Colab.objects.all()
    #research = Research.objects.prefetch_related("publication_research_set")
    research = Research.objects.defer("description", "content").prefetch_related(
        "publication_research_set"
    )
    home_config = HomePageConfiguration.objects.first()
    slides = HeroSlide.objects.filter(is_active=True).order_by("my_order")
    text = render(
        request,
        "home/home.html",
        {
            "object": query,
            "research": research,
            "home_config": home_config,
            "slides": slides,
        },
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
    project_alumni = ProjectAlumni.objects.all()
    team_page = TeamPage.objects.first()

    text = render(
        request,
        "home/team.html",
        {
            "phd": phd,
            "postdoc": postdoc,
            "project": project,
            "alumni": alumni,
            "project_alumni": project_alumni,
            "team_page": team_page,
        },
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


def research(request):
    research = Research.objects.prefetch_related("publication_research_set")

    for r in research:
        # r.publication = list(r.publication_research_set.values_list("link", flat=True))
        r.publication = [p.link for p in r.publication_research_set.all()]
    if sync:
        text = render(request, "home/research.html", {"research": research})
        with open("research.html", "wb") as f:
            f.write(text.content)
        return text
    return render(request, "home/research.html", {"research": research})


def research_detail(request, pk):
    research = get_object_or_404(Research, pk=pk)
    # research = Research.objects.prefetch_related("publication_research_set")
    return render(request, "home/research_detail.html", {"research": research})


def news(request):
    news = News.objects.all().order_by("-date")
    latest_publications = list(Publication.objects.all().order_by("-year", "-id")[:5])
    
    for pub in latest_publications:
        # Extract first author assuming comma or 'and' separation
        authors_list = pub.authors.replace(" and ", ",").split(",")
        pub.first_author = authors_list[0].strip() if authors_list else pub.authors

    text = render(request, "home/news.html", {"news": news, "latest_publications": latest_publications})
    if sync:
        with open("news.html", "wb") as f:
            f.write(text.content)
    return text


def publication(request):
    # publication = Publication.objects.all()
    publication = Publication.objects.all().order_by("id").reverse()
    text = render(request, "home/publication.html", {"publication": publication})
    if sync:
        with open("publication.html", "wb") as f:
            f.write(text.content)
    return text


def gallery(request):
    # Get data for all three sections
    photos = Gallery.objects.all().order_by("-date")
    animations = Animation.objects.all().order_by("-date")
    posters = Poster.objects.all().order_by("-date")

    context = {
        "photos": photos,
        "animations": animations,
        "posters": posters,
    }

    text = render(request, "home/gallery.html", context)

    # Keeping your sync logic
    if sync:
        with open("gallery.html", "wb") as f:
            f.write(text.content)

    return text


def softwares(request, sync_local=False):
    # Fetch all software projects from the database
    projects = SoftwareProject.objects.all().order_by("my_order")

    # Render the template with the projects context
    response = render(request, "home/softwares.html", {"projects": projects})

    # Optional: export rendered HTML for static use if sync_local=True
    if sync_local or sync:
        with open("softwares.html", "wb") as f:
            f.write(response.content)

    return response


def positions(request):
    text = render(request, "home/position.html")
    if sync:
        with open("positions.html", "wb") as f:
            f.write(text.content)
    return text
