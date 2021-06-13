from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('', views.index, name="homepage"),
	path('plans/', views.plans, name='plans'),
	path('dashboard/', views.dashboard, name="dashboard"),
	path('register/', views.register, name="register"),
	path('login', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('checkout/', views.subscribe, name='subscribe'),


]