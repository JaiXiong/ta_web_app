from django.conf.urls import url
from website import views


urlpatterns = [
    url(r'^$', views.Home.as_view()),
    url(r'^login/$', views.Login.as_view()),
    #url(r'^pizza/$', views.PizzaPageView.as_view()),
    #url(r'^icecream/$', views.IcecreamPageView.as_view()),
    #url(r'^purchase/$', views.PurchasecreamPageView.as_view())
]