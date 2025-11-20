from django.urls import path
from . import views

urlpatterns = [
    path("instructorlogincheck", views.instructorlogincheck, name="instructorlogincheck"),
    path("instructorhome", views.instructorhome, name="instructorhome"),
    path("instructorlogout", views.instructorlogout, name="instructorlogout"),
    path("instructorcourses", views.instructorcourses, name="instructorcourses"),
]
