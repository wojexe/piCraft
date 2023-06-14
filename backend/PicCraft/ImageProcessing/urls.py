from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path(r'^resize/?$', views.Resize.as_view()),
    re_path(r'^compress/?$', views.Compress.as_view()),
    re_path(r'^enhance/?$', views.Enhance.as_view()),
    re_path(r'^change_format/?$', views.ChangeFormat.as_view()),
    re_path(r'^combine/?$', views.Combine.as_view())
]