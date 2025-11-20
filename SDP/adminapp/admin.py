from django.contrib import admin
from .models import Admin, Alumni, Connection, Event, EventRegistration, JobPosting, Message

# Register your models here.
admin.site.register(Admin)
admin.site.register(Alumni)
admin.site.register(Connection)
admin.site.register(Event)
admin.site.register(EventRegistration)
admin.site.register(JobPosting)
admin.site.register(Message)
