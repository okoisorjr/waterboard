from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
	path('', views.index, name="homepage"),
	path('dashboard/', views.dashboard, name="dashboard"),
	path('register/', views.register, name="register"),
	path('activate/<uidb64>/<token>/', views.activate_account_view, name='account-activate'),
	path('login', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('checkout/', views.subscribe, name='subscribe'),
	path('installation-fee/', views.pay_installation_fee, name='installation'),


]