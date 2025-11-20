from django.db import models

# Create your models here.
class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    instructor_id = models.CharField(max_length=50, blank=False, unique=True)
    fullname = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=False, unique=True)
    contact = models.CharField(max_length=20, blank=False, unique=True)
    department = models.CharField(max_length=50, blank=False)
    specialization = models.CharField(max_length=100, blank=True)
    password = models.CharField(max_length=100, blank=False, default="Instructor123")
    profile_picture = models.ImageField(upload_to='instructor_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "instructor_table"
        
    def __str__(self):
        return f"{self.fullname} ({self.instructor_id})"
