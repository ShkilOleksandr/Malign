from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('podcasts/', views.podcasts, name='podcasts'),
]