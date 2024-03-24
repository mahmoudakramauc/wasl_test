# scholars/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Session, Lecture, Availability

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class SessionBookingForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date_time', 'duration']

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ['title', 'description']

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['start_time', 'end_time', 'day_of_week']  # Update fields as needed

