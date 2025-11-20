from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student
from adminapp.models import Alumni, Connection, Event, EventRegistration, JobPosting, Message
from django.db.models import Q
from django.utils import timezone

# Create your views here.

def studentlogincheck(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        
        try:
            student = Student.objects.get(student_id=student_id, password=password)
            request.session['student_id'] = student.id
            request.session['role'] = 'student'
            request.session['student_name'] = student.fullname
            messages.success(request, f'Welcome {student.fullname}!')
            return redirect('studenthome')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    return redirect('login')

def studentlogout(request):
    if 'role' in request.session:
        del request.session['role']
    if 'student_id' in request.session:
        del request.session['student_id']
    if 'student_name' in request.session:
        del request.session['student_name']
    messages.info(request, 'Logged out successfully!')
    return redirect('login')

def studenthome(request):
    if 'role' not in request.session or request.session['role'] != 'student':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = Student.objects.get(id=request.session['student_id'])
    
    context = {
        'student': student,
    }
    return render(request, 'student/studenthome.html', context)

def studentcourses(request):
    if 'role' not in request.session or request.session['role'] != 'student':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    messages.info(request, 'To access alumni network features, please login as Alumni using your Student ID and password.')
    return redirect('studenthome')

def availablecourses(request):
    if 'role' not in request.session or request.session['role'] != 'student':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    messages.info(request, 'To access alumni network features, please login as Alumni using your Student ID and password.')
    return redirect('studenthome')

# Alumni Authentication and Views
def alumnilogincheck(request):
    if request.method == 'POST':
        alumniid = request.POST.get('alumniid')
        password = request.POST.get('password')
        
        try:
            alumni = Alumni.objects.get(alumniid=int(alumniid), password=password)
            
            # Check if account is approved
            if not alumni.is_approved:
                messages.warning(request, 'Your account is pending admin approval. Please wait for approval before logging in.')
                return redirect('login')
            
            request.session['alumni_id'] = alumni.id
            request.session['role'] = 'alumni'
            request.session['alumni_name'] = alumni.fullname
            messages.success(request, f'Welcome {alumni.fullname}!')
            return redirect('alumnihome')
        except Alumni.DoesNotExist:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    return redirect('login')

def alumnilogout(request):
    if 'role' in request.session:
        del request.session['role']
    if 'alumni_id' in request.session:
        del request.session['alumni_id']
    if 'alumni_name' in request.session:
        del request.session['alumni_name']
    messages.info(request, 'Logged out successfully!')
    return redirect('login')

def alumnihome(request):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.get(id=request.session['alumni_id'])
    
    # Get statistics
    connections_count = Connection.objects.filter(
        Q(from_alumni=alumni, status='accepted') | Q(to_alumni=alumni, status='accepted')
    ).count()
    
    pending_requests = Connection.objects.filter(to_alumni=alumni, status='pending').count()
    
    upcoming_events = Event.objects.filter(
        is_active=True, 
        event_date__gte=timezone.now()
    ).order_by('event_date')[:5]
    
    recent_jobs = JobPosting.objects.filter(is_active=True).order_by('-posted_at')[:5]
    
    unread_messages = Message.objects.filter(receiver=alumni, is_read=False).count()
    
    context = {
        'alumni': alumni,
        'connections_count': connections_count,
        'pending_requests': pending_requests,
        'upcoming_events': upcoming_events,
        'recent_jobs': recent_jobs,
        'unread_messages': unread_messages,
    }
    return render(request, 'alumni/alumnihome.html', context)

def alumnidirectory(request):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.get(id=request.session['alumni_id'])
    all_alumni = Alumni.objects.exclude(id=alumni.id)
    
    # Get connection status for each alumni
    alumni_list = []
    for a in all_alumni:
        connection = Connection.objects.filter(
            Q(from_alumni=alumni, to_alumni=a) | Q(from_alumni=a, to_alumni=alumni)
        ).first()
        
        alumni_list.append({
            'alumni': a,
            'connection_status': connection.status if connection else None,
            'is_connected': connection and connection.status == 'accepted' if connection else False,
        })
    
    context = {
        'alumni_list': alumni_list,
        'current_alumni': alumni,
    }
    return render(request, 'alumni/alumnidirectory.html', context)

def sendconnection(request, alumni_id):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    from_alumni = Alumni.objects.get(id=request.session['alumni_id'])
    to_alumni = get_object_or_404(Alumni, id=alumni_id)
    
    # Check if connection already exists
    if Connection.objects.filter(from_alumni=from_alumni, to_alumni=to_alumni).exists():
        messages.warning(request, 'Connection request already sent!')
        return redirect('alumnidirectory')
    
    if Connection.objects.filter(from_alumni=to_alumni, to_alumni=from_alumni).exists():
        messages.warning(request, 'Connection request already exists!')
        return redirect('alumnidirectory')
    
    Connection.objects.create(from_alumni=from_alumni, to_alumni=to_alumni, status='pending')
    messages.success(request, f'Connection request sent to {to_alumni.fullname}!')
    return redirect('alumnidirectory')

def acceptconnection(request, connection_id):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    connection = get_object_or_404(Connection, id=connection_id)
    if connection.to_alumni.id != request.session['alumni_id']:
        messages.error(request, 'Unauthorized!')
        return redirect('connections')
    
    connection.status = 'accepted'
    connection.accepted_at = timezone.now()
    connection.save()
    messages.success(request, f'Connection accepted with {connection.from_alumni.fullname}!')
    return redirect('connections')

def rejectconnection(request, connection_id):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    connection = get_object_or_404(Connection, id=connection_id)
    if connection.to_alumni.id != request.session['alumni_id']:
        messages.error(request, 'Unauthorized!')
        return redirect('connections')
    
    connection.status = 'rejected'
    connection.delete()
    messages.info(request, 'Connection request rejected.')
    return redirect('connections')

def connections(request):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.get(id=request.session['alumni_id'])
    
    # Get all connections
    sent_connections = Connection.objects.filter(from_alumni=alumni)
    received_connections = Connection.objects.filter(to_alumni=alumni)
    
    # Get accepted connections
    accepted_connections = Connection.objects.filter(
        Q(from_alumni=alumni, status='accepted') | Q(to_alumni=alumni, status='accepted')
    )
    
    connected_alumni = []
    for conn in accepted_connections:
        if conn.from_alumni == alumni:
            connected_alumni.append(conn.to_alumni)
        else:
            connected_alumni.append(conn.from_alumni)
    
    # Pending requests
    pending_received = Connection.objects.filter(to_alumni=alumni, status='pending')
    pending_sent = Connection.objects.filter(from_alumni=alumni, status='pending')
    
    context = {
        'alumni': alumni,
        'connected_alumni': connected_alumni,
        'pending_received': pending_received,
        'pending_sent': pending_sent,
    }
    return render(request, 'alumni/connections.html', context)

def allevents_alumni(request):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.get(id=request.session['alumni_id'])
    events = Event.objects.filter(is_active=True).order_by('event_date')
    
    # Check registration status
    event_list = []
    for event in events:
        is_registered = EventRegistration.objects.filter(event=event, alumni=alumni).exists()
        registrations_count = EventRegistration.objects.filter(event=event).count()
        event_list.append({
            'event': event,
            'is_registered': is_registered,
            'registrations_count': registrations_count,
        })
    
    context = {
        'event_list': event_list,
        'alumni': alumni,
    }
    return render(request, 'alumni/allevents.html', context)

def registerevent(request, event_id):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.get(id=request.session['alumni_id'])
    event = get_object_or_404(Event, id=event_id)
    
    # Check if already registered
    if EventRegistration.objects.filter(event=event, alumni=alumni).exists():
        messages.warning(request, 'You are already registered for this event!')
        return redirect('allevents')
    
    # Check if event is full
    if event.max_attendees:
        current_registrations = EventRegistration.objects.filter(event=event).count()
        if current_registrations >= event.max_attendees:
            messages.error(request, 'Event is full!')
            return redirect('allevents')
    
    EventRegistration.objects.create(event=event, alumni=alumni)
    messages.success(request, f'Successfully registered for {event.title}!')
    return redirect('myevents')

def myevents(request):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.get(id=request.session['alumni_id'])
    registrations = EventRegistration.objects.filter(alumni=alumni).order_by('-registered_at')
    
    context = {
        'registrations': registrations,
        'alumni': alumni,
    }
    return render(request, 'alumni/myevents.html', context)

def jobboard(request):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    jobs = JobPosting.objects.filter(is_active=True).order_by('-posted_at')
    
    context = {
        'jobs': jobs,
    }
    return render(request, 'alumni/jobboard.html', context)

def jobdetails(request, job_id):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    job = get_object_or_404(JobPosting, id=job_id)
    
    context = {
        'job': job,
    }
    return render(request, 'alumni/jobdetails.html', context)

def messages_list(request):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.get(id=request.session['alumni_id'])
    
    # Get all conversations
    sent_messages = Message.objects.filter(sender=alumni)
    received_messages = Message.objects.filter(receiver=alumni)
    
    # Get unique contacts
    contacts = set()
    for msg in sent_messages:
        contacts.add(msg.receiver)
    for msg in received_messages:
        contacts.add(msg.sender)
    
    context = {
        'contacts': contacts,
        'alumni': alumni,
    }
    return render(request, 'alumni/messages.html', context)

def viewconversation(request, contact_id):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.get(id=request.session['alumni_id'])
    contact = get_object_or_404(Alumni, id=contact_id)
    
    # Get all messages between these two alumni
    conversation = Message.objects.filter(
        Q(sender=alumni, receiver=contact) | Q(sender=contact, receiver=alumni)
    ).order_by('sent_at')
    
    # Mark messages as read
    Message.objects.filter(sender=contact, receiver=alumni, is_read=False).update(
        is_read=True, read_at=timezone.now()
    )
    
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        content = request.POST.get('content')
        Message.objects.create(
            sender=alumni,
            receiver=contact,
            subject=subject,
            content=content
        )
        messages.success(request, 'Message sent!')
        return redirect('viewconversation', contact_id=contact_id)
    
    context = {
        'conversation': conversation,
        'contact': contact,
        'alumni': alumni,
    }
    return render(request, 'alumni/conversation.html', context)

def profile(request):
    if 'role' not in request.session or request.session['role'] != 'alumni':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    alumni = Alumni.objects.get(id=request.session['alumni_id'])
    
    if request.method == 'POST':
        alumni.current_position = request.POST.get('current_position', '')
        alumni.company = request.POST.get('company', '')
        alumni.location = request.POST.get('location', '')
        alumni.linkedin = request.POST.get('linkedin', '')
        alumni.bio = request.POST.get('bio', '')
        if 'profile_picture' in request.FILES:
            alumni.profile_picture = request.FILES['profile_picture']
        alumni.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'alumni': alumni,
    }
    return render(request, 'alumni/profile.html', context)
