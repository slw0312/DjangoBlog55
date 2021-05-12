from django.conf.urls import url

from home import views

urlpatterns = [
    url(r'^index/',views.index),
    url(r'^about/',views.about),
    url(r'^contact',views.contact),
    url(r'^gallery',views.gallery),
    url(r'^single_post',views.single_post),
]