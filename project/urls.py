from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name="homepage"),
	path('plans/', views.plans, name='plans'),
	path('dashboard/', views.dashboard, name="dashboard")

]