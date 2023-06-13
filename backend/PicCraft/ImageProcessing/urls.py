from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('resize',views.Resize.as_view()),
    path('compress',views.Compress.as_view()),
    path('enhance',views.Enhance.as_view()),
    path('change_format',views.ChangeFormat.as_view()),
    path('combine',views.Combine.as_view()),
    path('resize/', views.Resize.as_view()),
    path('compress/', views.Compress.as_view()),
    path('enhance/', views.Enhance.as_view()),
    path('change_format/', views.ChangeFormat.as_view()),
    path('combine/', views.Combine.as_view()),
]