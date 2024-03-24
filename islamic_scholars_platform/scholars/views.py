# scholars/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LectureForm, SessionBookingForm, AvailabilityForm
from .models import Scholar, Lecture, Session, Availability


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

    context = {
        'scholars': scholars,
        'sessions': sessions,
        'lectures': lectures,
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



@login_required
def book_session(request, scholar_id):
    if request.method == 'POST':
        form = SessionBookingForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.scholar_id = scholar_id
            session.user = request.user
            session.save()
            return redirect('session_booked')
    else:
        form = SessionBookingForm()
    return render(request, 'scholars/book_session.html', {'form': form})

@login_required
def session_booked(request):
    return render(request, 'scholars/session_booked.html')

