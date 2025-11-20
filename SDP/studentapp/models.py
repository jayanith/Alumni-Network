from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=50, blank=False, unique=True)
    fullname = models.CharField(max_length=100, blank=False)
    email = models.CharField(max_length=100, blank=False, unique=True)
    contact = models.CharField(max_length=20, blank=False, unique=True)
    department = models.CharField(max_length=50, blank=False)
    program = models.CharField(max_length=50, blank=False)
    year = models.IntegerField(blank=False)
    password = models.CharField(max_length=100, blank=False, default="Student123")
    profile_picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "student_table"
        
    def __str__(self):
        return f"{self.fullname} ({self.student_id})"
