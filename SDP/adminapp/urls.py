from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("adminlogincheck", views.adminlogincheck, name="adminlogincheck"),
    path("adminhome", views.adminhome, name="adminhome"),
    path("adminlogout", views.logout, name="adminlogout"),
    
    # Alumni CRUD
    path("addalumni", views.addalumni, name="addalumni"),
    path("allalumni", views.allalumni, name="allalumni"),
    path("editalumni/<int:alumni_id>", views.editalumni, name="editalumni"),
    path("deletealumni/<int:alumni_id>", views.deletealumni, name="deletealumni"),
    
    # Event CRUD
    path("addevent", views.addevent, name="addevent"),
    path("allevents", views.allevents, name="allevents"),
    path("editevent/<int:event_id>", views.editevent, name="editevent"),
    path("deleteevent/<int:event_id>", views.deleteevent, name="deleteevent"),
    
    # Job Posting CRUD
    path("addjob", views.addjob, name="addjob"),
    path("alljobs", views.alljobs, name="alljobs"),
    path("editjob/<int:job_id>", views.editjob, name="editjob"),
    path("deletejob/<int:job_id>", views.deletejob, name="deletejob"),
    
    # View Connections and Event Registrations
    path("viewconnections", views.viewconnections, name="viewconnections"),
    path("vieweventregistrations", views.vieweventregistrations, name="vieweventregistrations"),
    
    # Student CRUD
    path("addstudent", views.addstudent, name="addstudent"),
    path("allstudents", views.allstudents, name="allstudents"),
    path("editstudent/<int:student_id>", views.editstudent, name="editstudent"),
    path("deletestudent/<int:student_id>", views.deletestudent, name="deletestudent"),
    
    # Registration Approvals
    path("pendingregistrations", views.pendingregistrations, name="pendingregistrations"),
    path("approvestudent/<int:student_id>", views.approvestudent, name="approvestudent"),
    path("rejectstudent/<int:student_id>", views.rejectstudent, name="rejectstudent"),
    path("approvealumni/<int:alumni_id>", views.approvealumni, name="approvealumni"),
    path("rejectalumni/<int:alumni_id>", views.rejectalumni, name="rejectalumni"),
]
