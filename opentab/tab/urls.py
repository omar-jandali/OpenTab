from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.login_page, name='login'),
    url(r'^signup$', views.signup, name='signup'),
]
