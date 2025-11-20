from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Admin, Alumni, Connection, Event, EventRegistration, JobPosting, Message
from studentapp.models import Student
from django.utils import timezone
import hashlib
from datetime import datetime

# Create your views here.

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authentication Views
def adminlogincheck(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            admin = Admin.objects.get(username=username, password=password)
            request.session['admin_id'] = admin.id
            request.session['role'] = 'admin'
            messages.success(request, 'Login successful!')
            return redirect('adminhome')
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    return redirect('login')

def logout(request):
    if 'role' in request.session:
        del request.session['role']
    if 'admin_id' in request.session:
        del request.session['admin_id']
    messages.info(request, 'Logged out successfully!')
    return redirect('login')

# Dashboard
def adminhome(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    # Get statistics
    total_students = Student.objects.count()
    total_alumni = Alumni.objects.count()
    total_connections = Connection.objects.filter(status='accepted').count()
    total_events = Event.objects.filter(is_active=True).count()
    total_jobs = JobPosting.objects.filter(is_active=True).count()
    
    context = {
        'total_students': total_students,
        'total_alumni': total_alumni,
        'total_connections': total_connections,
        'total_events': total_events,
        'total_jobs': total_jobs,
    }
    return render(request, 'admin/adminhome.html', context)

# Alumni CRUD
def addalumni(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    if request.method == 'POST':
        alumniid = request.POST.get('alumniid')
        fullname = request.POST.get('fullname')
        gender = request.POST.get('gender')
        department = request.POST.get('department')
        program = request.POST.get('program')
        graduation_year = request.POST.get('graduation_year')
        current_position = request.POST.get('current_position', '')
        company = request.POST.get('company', '')
        location = request.POST.get('location', '')
        linkedin = request.POST.get('linkedin', '')
        bio = request.POST.get('bio', '')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password', 'Alumni123')
        
        try:
            Alumni.objects.create(
                alumniid=alumniid, fullname=fullname, gender=gender,
                department=department, program=program, graduation_year=graduation_year,
                current_position=current_position, company=company, location=location,
                linkedin=linkedin, bio=bio, email=email, contact=contact, password=password,
                is_approved=True  # Admin-added alumni are auto-approved
            )
            messages.success(request, 'Alumni added successfully!')
            return redirect('allalumni')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'admin/addalumni.html')

def allalumni(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.all().order_by('-created_at')
    return render(request, 'admin/allalumni.html', {'alumni': alumni})

def editalumni(request, alumni_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = get_object_or_404(Alumni, id=alumni_id)
    
    if request.method == 'POST':
        alumni.alumniid = request.POST.get('alumniid')
        alumni.fullname = request.POST.get('fullname')
        alumni.gender = request.POST.get('gender')
        alumni.department = request.POST.get('department')
        alumni.program = request.POST.get('program')
        alumni.graduation_year = request.POST.get('graduation_year')
        alumni.current_position = request.POST.get('current_position', '')
        alumni.company = request.POST.get('company', '')
        alumni.location = request.POST.get('location', '')
        alumni.linkedin = request.POST.get('linkedin', '')
        alumni.bio = request.POST.get('bio', '')
        alumni.email = request.POST.get('email')
        alumni.contact = request.POST.get('contact')
        if 'profile_picture' in request.FILES:
            alumni.profile_picture = request.FILES['profile_picture']
        alumni.save()
        messages.success(request, 'Alumni updated successfully!')
        return redirect('allalumni')
    
    return render(request, 'admin/editalumni.html', {'alumni': alumni})

def deletealumni(request, alumni_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = get_object_or_404(Alumni, id=alumni_id)
    alumni.delete()
    messages.success(request, 'Alumni deleted successfully!')
    return redirect('allalumni')

# Event CRUD
def addevent(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        event_date = request.POST.get('event_date')
        location = request.POST.get('location', '')
        event_type = request.POST.get('event_type', '')
        organizer_id = request.POST.get('organizer_id')
        max_attendees = request.POST.get('max_attendees')
        
        try:
            organizer = Alumni.objects.get(id=organizer_id) if organizer_id else None
            Event.objects.create(
                title=title, description=description, event_date=event_date,
                location=location, event_type=event_type, organizer=organizer,
                max_attendees=int(max_attendees) if max_attendees else None
            )
            messages.success(request, 'Event added successfully!')
            return redirect('allevents')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'admin/addevent.html', {'alumni': alumni})

def allevents(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    events = Event.objects.all().order_by('-event_date')
    return render(request, 'admin/allevents.html', {'events': events})

def editevent(request, event_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    event = get_object_or_404(Event, id=event_id)
    alumni = Alumni.objects.all()
    
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.description = request.POST.get('description', '')
        event.event_date = request.POST.get('event_date')
        event.location = request.POST.get('location', '')
        event.event_type = request.POST.get('event_type', '')
        organizer_id = request.POST.get('organizer_id')
        event.max_attendees = int(request.POST.get('max_attendees')) if request.POST.get('max_attendees') else None
        event.is_active = request.POST.get('is_active') == 'on'
        if organizer_id:
            event.organizer = Alumni.objects.get(id=organizer_id)
        event.save()
        messages.success(request, 'Event updated successfully!')
        return redirect('allevents')
    
    return render(request, 'admin/editevent.html', {'event': event, 'alumni': alumni})

def deleteevent(request, event_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, 'Event deleted successfully!')
    return redirect('allevents')

# Job Posting CRUD
def addjob(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')
        requirements = request.POST.get('requirements', '')
        posted_by_id = request.POST.get('posted_by')
        application_deadline = request.POST.get('application_deadline')
        contact_email = request.POST.get('contact_email', '')
        
        try:
            posted_by = Alumni.objects.get(id=posted_by_id)
            JobPosting.objects.create(
                title=title, company=company, location=location,
                description=description, requirements=requirements,
                posted_by=posted_by, application_deadline=application_deadline,
                contact_email=contact_email
            )
            messages.success(request, 'Job posting added successfully!')
            return redirect('alljobs')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'admin/addjob.html', {'alumni': alumni})

def alljobs(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    jobs = JobPosting.objects.all().order_by('-posted_at')
    return render(request, 'admin/alljobs.html', {'jobs': jobs})

def editjob(request, job_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    job = get_object_or_404(JobPosting, id=job_id)
    alumni = Alumni.objects.all()
    
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.company = request.POST.get('company')
        job.location = request.POST.get('location', '')
        job.description = request.POST.get('description', '')
        job.requirements = request.POST.get('requirements', '')
        job.posted_by = Alumni.objects.get(id=request.POST.get('posted_by'))
        job.application_deadline = request.POST.get('application_deadline')
        job.contact_email = request.POST.get('contact_email', '')
        job.is_active = request.POST.get('is_active') == 'on'
        job.save()
        messages.success(request, 'Job posting updated successfully!')
        return redirect('alljobs')
    
    return render(request, 'admin/editjob.html', {'job': job, 'alumni': alumni})

def deletejob(request, job_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    job = get_object_or_404(JobPosting, id=job_id)
    job.delete()
    messages.success(request, 'Job posting deleted successfully!')
    return redirect('alljobs')

# View Connections
def viewconnections(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    connections = Connection.objects.select_related('from_alumni', 'to_alumni').all().order_by('-created_at')
    return render(request, 'admin/viewconnections.html', {'connections': connections})

# View Event Registrations
def vieweventregistrations(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    registrations = EventRegistration.objects.select_related('event', 'alumni').all().order_by('-registered_at')
    return render(request, 'admin/vieweventregistrations.html', {'registrations': registrations})

# Student CRUD
def addstudent(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        department = request.POST.get('department')
        program = request.POST.get('program')
        year = request.POST.get('year')
        password = request.POST.get('password', 'Student123')
        gender = request.POST.get('gender', 'Other')
        
        try:
            # Create Student
            student =             Student.objects.create(
                student_id=student_id,
                fullname=fullname,
                email=email,
                contact=contact,
                department=department,
                program=program,
                year=int(year),
                password=password,
                is_approved=True  # Admin-added students are auto-approved
            )
            
            # Also create Alumni record with same credentials so student can login as both
            current_year = datetime.now().year
            graduation_year = current_year + (4 - int(year)) if int(year) <= 4 else current_year + 1
            
            # Convert student_id to integer for alumniid (handle both numeric and alphanumeric IDs)
            try:
                alumniid_value = int(student_id)
            except ValueError:
                # If student_id is not numeric, use a hash or convert to numeric representation
                # For simplicity, we'll use the hash of the string as a numeric value
                alumniid_value = abs(hash(student_id)) % (10 ** 10)  # Convert to 10-digit number
            
            Alumni.objects.create(
                alumniid=alumniid_value,
                fullname=fullname,
                gender=gender,
                department=department,
                program=program,
                graduation_year=graduation_year,
                email=email,
                contact=contact,
                password=password,  # Same password
                is_approved=True  # Admin-added alumni are auto-approved
            )
            
            messages.success(request, f'Student added successfully! They can now login as both Student (ID: {student_id}) and Alumni (ID: {alumniid_value}) with the same password.')
            return redirect('allstudents')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'admin/addstudent.html')

def allstudents(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    students = Student.objects.all().order_by('-created_at')
    return render(request, 'admin/allstudents.html', {'students': students})

def editstudent(request, student_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.student_id = request.POST.get('student_id')
        student.fullname = request.POST.get('fullname')
        student.email = request.POST.get('email')
        student.contact = request.POST.get('contact')
        student.department = request.POST.get('department')
        student.program = request.POST.get('program')
        student.year = int(request.POST.get('year'))
        if request.POST.get('password'):
            student.password = request.POST.get('password')
        if 'profile_picture' in request.FILES:
            student.profile_picture = request.FILES['profile_picture']
        student.save()
        
        # Update corresponding Alumni record if exists
        try:
            # Try to find alumni by converting student_id to int
            try:
                alumniid_value = int(student.student_id)
            except ValueError:
                alumniid_value = abs(hash(student.student_id)) % (10 ** 10)
            
            alumni = Alumni.objects.get(alumniid=alumniid_value)
            alumni.fullname = student.fullname
            alumni.email = student.email
            alumni.contact = student.contact
            alumni.department = student.department
            alumni.program = student.program
            if request.POST.get('password'):
                alumni.password = request.POST.get('password')
            alumni.save()
        except Alumni.DoesNotExist:
            pass
        except Alumni.MultipleObjectsReturned:
            # If multiple found, update the first one
            try:
                alumniid_value = int(student.student_id)
            except ValueError:
                alumniid_value = abs(hash(student.student_id)) % (10 ** 10)
            alumni = Alumni.objects.filter(alumniid=alumniid_value).first()
            if alumni:
                alumni.fullname = student.fullname
                alumni.email = student.email
                alumni.contact = student.contact
                alumni.department = student.department
                alumni.program = student.program
                if request.POST.get('password'):
                    alumni.password = request.POST.get('password')
                alumni.save()
        
        messages.success(request, 'Student updated successfully!')
        return redirect('allstudents')
    
    return render(request, 'admin/editstudent.html', {'student': student})

def deletestudent(request, student_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = get_object_or_404(Student, id=student_id)
    student_id_value = student.student_id
    
    # Delete corresponding Alumni record if exists
    try:
        try:
            alumniid_value = int(student_id_value)
        except ValueError:
            alumniid_value = abs(hash(student_id_value)) % (10 ** 10)
        
        alumni = Alumni.objects.get(alumniid=alumniid_value)
        alumni.delete()
    except (Alumni.DoesNotExist, Alumni.MultipleObjectsReturned):
        # If not found or multiple, try to delete all matching
        try:
            alumniid_value = int(student_id_value)
        except ValueError:
            alumniid_value = abs(hash(student_id_value)) % (10 ** 10)
        Alumni.objects.filter(alumniid=alumniid_value).delete()
    
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('allstudents')

# Registration Approval Views
def pendingregistrations(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    pending_students = Student.objects.filter(is_approved=False).order_by('-created_at')
    pending_alumni = Alumni.objects.filter(is_approved=False).order_by('-created_at')
    
    return render(request, 'admin/pendingregistrations.html', {
        'pending_students': pending_students,
        'pending_alumni': pending_alumni
    })

def approvestudent(request, student_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = get_object_or_404(Student, id=student_id)
    student.is_approved = True
    student.save()
    
    # Also approve corresponding Alumni record
    try:
        try:
            alumniid_value = int(student.student_id)
        except ValueError:
            alumniid_value = abs(hash(student.student_id)) % (10 ** 10)
        
        alumni = Alumni.objects.filter(alumniid=alumniid_value).first()
        if alumni:
            alumni.is_approved = True
            alumni.save()
    except:
        pass
    
    messages.success(request, f'Student {student.fullname} approved successfully!')
    return redirect('pendingregistrations')

def rejectstudent(request, student_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = get_object_or_404(Student, id=student_id)
    student_name = student.fullname
    
    # Delete corresponding Alumni record if exists
    try:
        try:
            alumniid_value = int(student.student_id)
        except ValueError:
            alumniid_value = abs(hash(student.student_id)) % (10 ** 10)
        Alumni.objects.filter(alumniid=alumniid_value).delete()
    except:
        pass
    
    student.delete()
    messages.success(request, f'Student {student_name} registration rejected and removed.')
    return redirect('pendingregistrations')

def approvealumni(request, alumni_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = get_object_or_404(Alumni, id=alumni_id)
    alumni.is_approved = True
    alumni.save()
    
    messages.success(request, f'Alumni {alumni.fullname} approved successfully!')
    return redirect('pendingregistrations')

def rejectalumni(request, alumni_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = get_object_or_404(Alumni, id=alumni_id)
    alumni_name = alumni.fullname
    alumni.delete()
    
    messages.success(request, f'Alumni {alumni_name} registration rejected and removed.')
    return redirect('pendingregistrations')
