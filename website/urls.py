from django.conf.urls import url
from website import views


urlpatterns = [
    url(r'^$', views.Home.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^search/$', views.Search.as_view()),
]