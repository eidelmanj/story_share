from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login_page, name='login_page'),
    url(r'^logout/', views.logout_page, name='logout_page'),
    url(r'^register/', views.register_page, name='register_page'),
    url(r'^generate_user/', views.generate_user, name='generate_user'),
    url(r'^authenticate/', views.authentication_page, name='authentication_page'),
    url(r'^upload/', views.upload_file, name='upload_file'),
    url(r'^user_page/', views.user_page, name='user_page'),
    url(r'^compile/', views.compilation_page, name='compilation_page'),
    url(r'^generate_compiled_stories/', views.generate_compiled_stories, name='generate_compiled_stories'),
    url(r'^compile_success/', views.compile_success, name='compile_success'),
    url(r'^upload_audio/', views.upload_audio_page, name='upload_audio_page'),
    url(r'^get_cities/', views.get_cities_ajax, name='get_cities_ajax'),
    url(r'^get_compilations/', views.get_compilations_ajax, name='get_compilations_ajax'),
    url(r'^rank_compilation/', views.rank_compilation_ajax, name='rank_compilation_ajax'),
    url(r'^rank_story/', views.rank_story_ajax, name='rank_story_ajax'),



    url(r'^testdb/', views.buildTestDb, name='buildTestDb'),
]
