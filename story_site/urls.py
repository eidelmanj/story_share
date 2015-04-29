from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_page, name='login_page'),
    url(r'^logout/', views.logout_page, name='logout_page'),
    url(r'^register/', views.register_page, name='register_page'),
    url(r'^generate_user/', views.generate_user, name='generate_user'),
    url(r'^authenticate/', views.authentication_page, name='authentication_page')
]
