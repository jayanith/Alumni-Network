from django.urls import path
from . import views

urlpatterns = [
    # Student routes
    path("studentlogincheck", views.studentlogincheck, name="studentlogincheck"),
    path("studenthome", views.studenthome, name="studenthome"),
    path("studentlogout", views.studentlogout, name="studentlogout"),
    path("studentcourses", views.studentcourses, name="studentcourses"),
    path("availablecourses", views.availablecourses, name="availablecourses"),
    
    # Alumni routes
    path("alumnilogincheck", views.alumnilogincheck, name="alumnilogincheck"),
    path("alumnihome", views.alumnihome, name="alumnihome"),
    path("alumnilogout", views.alumnilogout, name="alumnilogout"),
    path("alumnidirectory", views.alumnidirectory, name="alumnidirectory"),
    path("connections", views.connections, name="connections"),
    path("sendconnection/<int:alumni_id>", views.sendconnection, name="sendconnection"),
    path("acceptconnection/<int:connection_id>", views.acceptconnection, name="acceptconnection"),
    path("rejectconnection/<int:connection_id>", views.rejectconnection, name="rejectconnection"),
    path("allevents", views.allevents_alumni, name="allevents"),
    path("registerevent/<int:event_id>", views.registerevent, name="registerevent"),
    path("myevents", views.myevents, name="myevents"),
    path("jobboard", views.jobboard, name="jobboard"),
    path("jobdetails/<int:job_id>", views.jobdetails, name="jobdetails"),
    path("messages", views.messages_list, name="messages"),
    path("viewconversation/<int:contact_id>", views.viewconversation, name="viewconversation"),
    path("profile", views.profile, name="profile"),
]
