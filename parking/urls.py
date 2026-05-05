from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home),
    path('book/<int:id>/', views.book_slot),
    path('exit/<int:id>/', views.exit_slot),
    path('login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('dashboard/', views.dashboard),
]