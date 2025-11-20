from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from studentapp.models import Student
from adminapp.models import Alumni
from datetime import datetime
import hashlib

def demofunction(request):
    return HttpResponse("Alumni Networking and Relationship Management System")
def demofunction1(request):
    return HttpResponse("<h3>Alumni Network Platform</h3>")
def demofunction2(request):
    return HttpResponse("<font color='green'>Connect, Network, Grow Together</font>")
def homefunction(request):
    return render(request,"index.html")
def aboutfunction(request):
    return render(request,"about.html")
def loginfunction(request):
    return render(request,"login.html")
def contactfunction(request):
    return render(request,"contact.html")

# Registration Views
def register_student(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        department = request.POST.get('department')
        program = request.POST.get('program')
        year = request.POST.get('year')
        password = request.POST.get('password')
        gender = request.POST.get('gender', 'Other')
        
        try:
            # Check if student already exists
            if Student.objects.filter(student_id=student_id).exists():
                messages.error(request, 'Student ID already exists!')
                return render(request, 'register_student.html')
            
            if Student.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered!')
                return render(request, 'register_student.html')
            
            # Create Student (pending approval)
            student = Student.objects.create(
                student_id=student_id,
                fullname=fullname,
                email=email,
                contact=contact,
                department=department,
                program=program,
                year=int(year),
                password=password,
                is_approved=False
            )
            
            # Also create Alumni record (pending approval) so they can login as Alumni once approved
            current_year = datetime.now().year
            graduation_year = current_year + (4 - int(year)) if int(year) <= 4 else current_year + 1
            
            try:
                alumniid_value = int(student_id)
            except ValueError:
                alumniid_value = abs(hash(student_id)) % (10 ** 10)
            
            Alumni.objects.create(
                alumniid=alumniid_value,
                fullname=fullname,
                gender=gender,
                department=department,
                program=program,
                graduation_year=graduation_year,
                email=email,
                contact=contact,
                password=password,
                is_approved=False
            )
            
            messages.success(request, 'Registration successful! Your account is pending admin approval. You will be notified once approved.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'register_student.html')

def register_alumni(request):
    if request.method == 'POST':
        alumniid = request.POST.get('alumniid')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        department = request.POST.get('department')
        program = request.POST.get('program')
        graduation_year = request.POST.get('graduation_year')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        current_position = request.POST.get('current_position', '')
        company = request.POST.get('company', '')
        location = request.POST.get('location', '')
        linkedin = request.POST.get('linkedin', '')
        bio = request.POST.get('bio', '')
        
        try:
            # Check if alumni already exists
            if Alumni.objects.filter(alumniid=alumniid).exists():
                messages.error(request, 'Alumni ID already exists!')
                return render(request, 'register_alumni.html')
            
            if Alumni.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered!')
                return render(request, 'register_alumni.html')
            
            # Create Alumni (pending approval)
            Alumni.objects.create(
                alumniid=int(alumniid),
                fullname=fullname,
                gender=gender,
                department=department,
                program=program,
                graduation_year=int(graduation_year),
                current_position=current_position,
                company=company,
                location=location,
                linkedin=linkedin,
                bio=bio,
                email=email,
                contact=contact,
                password=password,
                is_approved=False
            )
            
            messages.success(request, 'Registration successful! Your account is pending admin approval. You will be notified once approved.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Registration failed: {str(e)}')
    
    return render(request, 'register_alumni.html')
