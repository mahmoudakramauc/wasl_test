# scholars/admin.py
from django.contrib import admin
from .models import Scholar, Lecture, Session, Availability

admin.site.register(Scholar)
admin.site.register(Lecture)
admin.site.register(Session)
admin.site.register(Availability)
