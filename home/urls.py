# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

# from django.conf.urls import  url
# from django.views.generic import TemplateView
# handler404 = 'error_404'

urlpatterns = [
    path("", views.home, name="home"),
    path("team", views.team, name="team"),
    path("contacts", views.contacts, name="contacts"),
    path("gallery", views.gallery, name="gallery"),
    path("news", views.news, name="news"),
    path("research", views.research, name="research"),
    path("publication", views.publication, name="publication"),
    path("softwares", views.softwares, name="softwares"),
    path("positions", views.positions, name="positions"),
]
# urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
