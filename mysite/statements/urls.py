from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login_user/', views.loginAccount, name = "login"),
    # path('register/', views.register, name = 'register'),
    # path('update/', views.updateAccount, name = 'updateAccount'),
    # path('update/password', views.changePassword, name = 'changePassword'),
    # path('delete/', views.deleteAccount, name = 'deleteAccount'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('send_email/', views.send_email, name='send_email'),
]
