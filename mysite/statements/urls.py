from django.urls import path
from . import views

app_name = 'statements'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('view-statement/', views.view_statement, name = 'view_statement'),
    path('login_user/', views.loginAccount, name = "login"),
    # path('register/', views.register, name = 'register'),
    # path('update/', views.updateAccount, name = 'updateAccount'),
    # path('update/password', views.changePassword, name = 'changePassword'),
    # path('delete/', views.deleteAccount, name = 'deleteAccount'),
    path('send_email/', views.send_email, name='send_email'),
    path('print_statement/', views.print_statement, name='print_statement')
]
