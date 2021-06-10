from django.urls import path
from . import views

urlpatterns = [
	path('index/', views.index),
	path('subscription/', views.subscription),
	path('dashboard/', views.dashboard)]