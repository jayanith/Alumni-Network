from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Instructor

# Create your views here.

def instructorlogincheck(request):
    if request.method == 'POST':
        instructor_id = request.POST.get('instructor_id')
        password = request.POST.get('password')
        
        try:
            instructor = Instructor.objects.get(instructor_id=instructor_id, password=password)
            request.session['instructor_id'] = instructor.id
            request.session['role'] = 'instructor'
            request.session['instructor_name'] = instructor.fullname
            messages.success(request, f'Welcome {instructor.fullname}!')
            return redirect('instructorhome')
        except Instructor.DoesNotExist:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    return redirect('login')

def instructorlogout(request):
    if 'role' in request.session:
        del request.session['role']
    if 'instructor_id' in request.session:
        del request.session['instructor_id']
    if 'instructor_name' in request.session:
        del request.session['instructor_name']
    messages.info(request, 'Logged out successfully!')
    return redirect('login')

def instructorhome(request):
    if 'role' not in request.session or request.session['role'] != 'instructor':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    instructor = Instructor.objects.get(id=request.session['instructor_id'])
    
    context = {
        'instructor': instructor,
    }
    return render(request, 'instructor/instructorhome.html', context)

def instructorcourses(request):
    if 'role' not in request.session or request.session['role'] != 'instructor':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    messages.info(request, 'To access alumni network features, please login as Alumni.')
    return redirect('instructorhome')
