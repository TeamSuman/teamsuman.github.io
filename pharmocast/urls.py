
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="pharmocast"),
    path("test", views.test, name="test"),
    path('contact', views.contact, name='contact'),
    # path('Gallery', views.gallery, name='gallery'),
    # path('code1', views.code1, name='code1'),
]
# urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
