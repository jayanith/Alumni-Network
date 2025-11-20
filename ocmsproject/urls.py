"""
URL configuration for ocmsproject project.
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.demofunction, name="demo"),
    path("demo", views.demofunction1, name="demo1"),
    path("demo1", views.demofunction2, name="demo2"),
    path("home", views.homefunction, name="home"),
    path("about", views.aboutfunction, name="about"),
    path("login", views.loginfunction, name="login"),
    path("contact", views.contactfunction, name="contact"),
    path("register-student", views.register_student, name="register_student"),
    path("register-alumni", views.register_alumni, name="register_alumni"),
    path("", include("adminapp.urls")),
    path("", include("instructorapp.urls")),
    path("", include("studentapp.urls")),
]
