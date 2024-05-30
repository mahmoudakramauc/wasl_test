# scholars/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LectureForm, SessionBookingForm, AvailabilityForm, SessionEditForm
from .models import Scholar, Lecture, Session, Availability
from django.utils import timezone
from datetime import datetime
from .forms import BookingForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('scholar_dashboard')  # Redirect to a page after login (e.g., scholar list)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

@login_required
def scholar_list(request):
    scholars = Scholar.objects.all()
    return render(request, 'scholars/scholar_list.html', {'scholars': scholars})

def about(request):
    return render(request, 'about.html')

@login_required
def home(request):
    scholars = Scholar.objects.all()
    sessions = Session.objects.all()  # Fetch all sessions for display
    lectures = Lecture.objects.all()  # Fetch all lectures
    user_sessions = Session.objects.filter(user=request.user)

    context = {
        'scholars': scholars,
        'sessions': sessions,
        'lectures': lectures,
        'user_sessions': user_sessions,

    }
    return render(request, 'scholars/home.html', context)

@login_required
def scholar_dashboard(request):
    if request.user.is_authenticated and hasattr(request.user, 'scholar'):
        scholar = request.user.scholar
        lectures = Lecture.objects.filter(associated_scholar=scholar.user)
        sessions = Session.objects.filter(scholar=scholar.user)
        availability = Availability.objects.filter(scholar=scholar.user)  # Retrieve scholar's availability
        # Initialize form variables
        lecture_form = LectureForm()
        session_form = SessionBookingForm()
        availability_form = AvailabilityForm()

        if request.method == 'POST':
            if 'lecture_form' in request.POST:
                lecture_form = LectureForm(request.POST)
                if lecture_form.is_valid():
                    lecture = lecture_form.save(commit=False)
                    lecture.associated_scholar = scholar.user
                    lecture.save()
                    return redirect('scholar_dashboard')
            elif 'session_form' in request.POST:
                session_form = SessionBookingForm(request.POST)
                if session_form.is_valid():
                    session = session_form.save(commit=False)
                    session.scholar = scholar.user
                    session.save()
                    return redirect('scholar_dashboard')

            elif 'availability_form' in request.POST:
                availability_form = AvailabilityForm(request.POST)
                if availability_form.is_valid():
                    availability = availability_form.save(commit=False)
                    availability.scholar = scholar.user
                    availability.save()
                    return redirect('scholar_dashboard')
                 
        else:
            lecture_form = LectureForm()
            session_form = SessionBookingForm()
            availability_form = AvailabilityForm()

        context = {
            'lectures': lectures,
            'sessions': sessions,
            'lecture_form': lecture_form,
            'session_form': session_form,
            'availability': availability,
            'availability_form': availability_form,

        }
        return render(request, 'scholars/scholar_dashboard.html', context)
    else:
        return redirect('home')  # Redirect non-scholars to the home page


@login_required
def add_lecture(request):
    if request.method == 'POST':
        form = LectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.associated_scholar = request.user.scholar.user # Associate the lecture with the current scholar
            lecture.save()
            return redirect('scholar_dashboard')  # Redirect to scholar dashboard or any other page
    else:
        form = LectureForm()
    return render(request, 'scholars/add_lecture.html', {'form': form})

@login_required
def edit_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    if request.method == 'POST':
        form = LectureForm(request.POST, instance=lecture)
        if form.is_valid():
            form.save()
            return redirect('scholar_dashboard')
    else:
        form = LectureForm(instance=lecture)
    return render(request, 'scholars/edit_lecture.html', {'form': form})

@login_required
def delete_lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    if request.method == 'POST':
        lecture.delete()
        return redirect('scholar_dashboard')
    return render(request, 'scholars/delete_lecture_confirm.html', {'lecture': lecture})



@login_required
def add_availability(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.scholar = request.user.scholar.user  # Associate availability with the current scholar
            availability.save()
            return redirect('scholar_dashboard')
    else:
        form = AvailabilityForm()
    return render(request, 'scholars/add_availability.html', {'form': form})

@login_required
def edit_availability(request, availability_id):
    availability = get_object_or_404(Availability, pk=availability_id)
    if request.method == 'POST':
        form = AvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            return redirect('scholar_dashboard')
    else:
        form = AvailabilityForm(instance=availability)
    return render(request, 'scholars/edit_availability.html', {'form': form})

@login_required
def delete_availability(request, availability_id):
    availability = get_object_or_404(Availability, pk=availability_id)
    if request.method == 'POST':
        availability.delete()
        return redirect('scholar_dashboard')
    return render(request, 'scholars/delete_availability_confirm.html', {'availability': availability})



def scholar_availability_list(request):
    scholars = Scholar.objects.all()
    availability_data = []
    for scholar in scholars:
        availability_slots = Availability.objects.filter(scholar=scholar)
        availability_data.append({
            'scholar': scholar,
            'availability': availability_slots
        })
    return render(request, 'scholar_availability_list.html', {'availability_data': availability_data})


def scholar_detail(request, scholar_id):
    scholar = get_object_or_404(Scholar, pk=scholar_id)
    return render(request, 'scholars/scholar_detail.html', {'scholar': scholar})
    
@login_required
def book_session(request, scholar_id):
    scholar = get_object_or_404(Scholar, pk=scholar_id)
    availabilities = scholar.user.availabilities.all()  # Get all availabilities for the scholar

    if request.method == 'POST':
        form = SessionBookingForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            scholar = get_object_or_404(Scholar, pk=scholar_id)
            user_instance = scholar.user  # Retrieve the User instance associated with the scholar
            availability = Availability.objects.filter(
                scholar=user_instance,
                day_of_week=session.date_time.strftime('%A'),
                start_time__lte=session.date_time.time(),
                end_time__gte=session.date_time.time()
            ).exists()
            if not availability:
                messages.error(request, 'The scholar is not available at the requested time.')
                return redirect('scholar_dashboard')
            
            session.scholar_id = scholar_id
            session.user = request.user
            session.save()
            return redirect('session_booked')
    else:
        form = SessionBookingForm()
        # Generate a range of numbers for duration
        duration_range = range(15, 61, 15)  # Numbers from 15 to 60 with a step of 15

        context = {
        'form': form,
        'availabilities': availabilities,
        'duration_range': duration_range,
    }
    return render(request, 'scholars/book_session.html', context)

@login_required
def session_booked(request):
    return render(request, 'scholars/session_booked.html')


def confirm_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    
    # Check if the user is the scholar associated with the session
    if request.user == session.scholar:
        confirmation_status = request.POST.get('confirmation_status')
        
        # Handle confirmation or rejection based on the button clicked
        if confirmation_status == 'confirm':
            session.is_confirmed = True
            session.save()
            messages.success(request, 'Session confirmed successfully.')
        elif confirmation_status == 'reject':
            session.is_confirmed = False
            session.save()
            messages.warning(request, 'Session rejected.')
        else:
            messages.error(request, 'Invalid action.')
        
        return redirect('scholar_dashboard')
    else:
        # Optionally, add an error message if the session doesn't belong to the current user
        messages.error(request, 'You are not authorized to confirm this session.')
        return redirect('scholar_dashboard')  # Redirect to dashboard in case of unauthorized access



# def confirm_session(request, session_id):
#     session = get_object_or_404(Session, pk=session_id)

#     if request.method == 'POST':
#         if 'confirm' in request.POST:
#             session.is_confirmed = True
#         elif 'reject' in request.POST:
#             session.is_confirmed = False
        
#         session.save()
#         # Redirect to a page indicating the confirmation status
#         return redirect('session_detail', session_id=session_id)

#     return render(request, 'confirm_session.html', {'session': session})

def edit_session(request, session_id):
    # Retrieve the session object to be edited
    session = get_object_or_404(Session, pk=session_id)

    if request.method == 'POST':
        # If form is submitted with data, process the form
        form = SessionEditForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            # Redirect to a suitable page after successful update
            return redirect('scholar_dashboard')
    else:
        # If it's a GET request, populate the form with session data
        form = SessionEditForm(instance=session)

    return render(request, 'scholars/edit_session.html', {'form': form})



def session_detail(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    return render(request, 'scholars/session_detail.html', {'session': session})

def cancel_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    
    # Check if the session belongs to the current user
    if session.scholar == request.user:
        # Delete the session
        session.delete()
        # Optionally, add a success message
        messages.success(request, 'Session cancelled successfully.')
        return redirect('session_cancelled')
    else:
        # Optionally, add an error message if the session doesn't belong to the current user
        messages.error(request, 'You are not authorized to cancel this session.')
    
    return redirect('session_booked')
def session_cancelled(request):
    return render(request, 'scholars/cancelled_session.html')
