# scholars/models.py
from django.db import models
from django.contrib.auth.models import User

class Lecture(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    associated_scholar = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='scholar_images/', null=True, blank=True)
    location = models.CharField(max_length=100, default='')  # Add the location field
    def __str__(self):
        return self.title

class Scholar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    specialization = models.CharField(max_length=100)
    lectures = models.ManyToManyField(Lecture)
    image = models.ImageField(upload_to='scholar_images/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Session(models.Model):
    scholar = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_sessions')
    date_time = models.DateTimeField()
    duration = models.IntegerField()  # Duration in minutes
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Session with {self.scholar.username} on {self.date_time}"
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.session}"
        
class Availability(models.Model):
    DAY_CHOICES = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
        # Add other days of the week as needed
    ]
    scholar = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES, default='Sunday')
    start_time = models.TimeField(default='00:00')  # Default to midnight
    end_time = models.TimeField(default='23:59')    # Default to just before midnight
    duration = models.IntegerField(default=60)      # Duration in minutes, default to 60 minutes

    def __str__(self):
        return f"Availability for {self.scholar.username} on {self.day_of_week} from {self.start_time} to {self.end_time}"

