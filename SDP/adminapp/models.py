from django.db import models
from django.utils import timezone

# Create your models here.
class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100,blank=False,unique=True)
    password=models.CharField(max_length=100,blank=False)

    class Meta:
        db_table="admin_table"
        
class Alumni(models.Model):
    id=models.AutoField(primary_key=True)
    alumniid=models.BigIntegerField(blank=False,unique=True)
    fullname=models.CharField(max_length=100,blank=False)
    gender=models.CharField(max_length=20,blank=False)
    department=models.CharField(max_length=50,blank=False)
    program = models.CharField(max_length=50, blank=False)
    graduation_year = models.IntegerField(blank=False)
    current_position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    password=models.CharField(max_length=100,blank=False,default="Alumni123")
    email=models.CharField(max_length=100,blank=False,unique=True)
    contact=models.CharField(max_length=20,blank=False,unique=True)
    profile_picture = models.ImageField(upload_to='alumni_profiles/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "alumni_table"
        
    def __str__(self):
        return f"{self.fullname} ({self.alumniid})"

class Connection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    id = models.AutoField(primary_key=True)
    from_alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='sent_connections')
    to_alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='received_connections')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "connection_table"
        unique_together = ['from_alumni', 'to_alumni']
        
    def __str__(self):
        return f"{self.from_alumni.fullname} -> {self.to_alumni.fullname} ({self.status})"

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=True)
    event_date = models.DateTimeField(blank=False)
    location = models.CharField(max_length=200, blank=True)
    event_type = models.CharField(max_length=50, blank=True)  # networking, workshop, reunion, etc.
    organizer = models.ForeignKey(Alumni, on_delete=models.SET_NULL, null=True, blank=True, related_name='organized_events')
    max_attendees = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "event_table"
        
    def __str__(self):
        return f"{self.title} - {self.event_date}"

class EventRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    alumni = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='event_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "event_registration_table"
        unique_together = ['event', 'alumni']
        
    def __str__(self):
        return f"{self.alumni.fullname} - {self.event.title}"

class JobPosting(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False)
    company = models.CharField(max_length=100, blank=False)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    posted_by = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='job_postings')
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    contact_email = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = "job_posting_table"
        
    def __str__(self):
        return f"{self.title} at {self.company}"

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Alumni, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = "message_table"
        ordering = ['-sent_at']
        
    def __str__(self):
        return f"{self.sender.fullname} -> {self.receiver.fullname}: {self.subject}"
