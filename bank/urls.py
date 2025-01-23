from . import views
from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('home/', views.home , name='bank-home'),
   path('run-tkinter/', views.run_tkinter, name='run_tkinter'),
]



# accounts/urls.py