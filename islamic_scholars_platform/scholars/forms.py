# scholars/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Session, Lecture, Availability, Scholar, UserSession

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class BookingForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date_time', 'duration']

class SessionBookingForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date_time', 'duration']

class SessionEditForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date_time', 'duration', 'is_confirmed']

class SessionCancellationForm(forms.ModelForm):
    class Meta:
        model = UserSession
        fields = ['is_cancelled']

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description', 'associated_scholar', 'image', 'location']

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['start_time', 'end_time', 'day_of_week']  # Update fields as needed

class ScholarForm(forms.ModelForm):
    class Meta:
        model = Scholar
        fields = ['bio', 'specialization', 'image']