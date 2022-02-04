from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login_user/', views.loginAccount, name = "login"),
    path('register/', views.register, name = 'register'),
    path('update/', views.updateAccount, name = 'updateAccount'),
    path('delete/', views.deleteAccount, name = 'deleteAccount')
]
