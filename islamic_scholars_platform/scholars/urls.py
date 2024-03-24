# scholars/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('<int:scholar_id>/book-session/', views.book_session, name='book_session'),
    path('session-booked/', views.session_booked, name='session_booked'),
    path('scholar-list/', views.scholar_list, name='scholar_list'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('add-lecture/', views.add_lecture, name='add_lecture'),
    path('edit-lecture/<int:lecture_id>/', views.edit_lecture, name='edit_lecture'),
    path('delete-lecture/<int:lecture_id>/', views.delete_lecture, name='delete_lecture'),
    path('scholar-dashboard/', views.scholar_dashboard, name='scholar_dashboard'),
    # Other URL patterns...
    path('book-session/', views.book_session, name='book_session'),
    path('session-booked/', views.session_booked, name='session_booked'),
    path('add-availability/', views.add_availability, name='add_availability'),
    path('edit-availability/<int:availability_id>/', views.edit_availability, name='edit_availability'),
    path('delete-availability/<int:availability_id>/', views.delete_availability, name='delete_availability'),
]
