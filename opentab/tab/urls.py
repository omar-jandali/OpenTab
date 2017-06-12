from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.login_page, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^loggedin$', views.logged_in, name='logged_in'),
    url(r'^logout$', views.logout_page, name='logout_page'),
]
