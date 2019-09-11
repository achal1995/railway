from django.conf.urls import url

from . import views

urlpatterns = [
    url('^register/$', views.register),
    #To activate user account
    url(r'^activate/(?P<uid>[\s\S]+)\/(?P<token>[\s\S]+)\/$',views.activate, name='activate'),
    #To send user password reset link
    url(r'^password-reset/$',views.password_reset, name='password_reset'),
    #To handle user password reset workflow
    url(r'^password-reset/confirm/(?P<uid>[\s\S]+)\/(?P<token>[\s\S]+)\/$',views.reset, name='reset'),

]