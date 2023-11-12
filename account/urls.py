from django.urls import path

from . import views


app_name = "account"

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('logout/', views.logout_user, name='logout'),
    path('edit-profile/', views.edit_account, name='edit_account'),
    path('verify/', views.verify_view, name='verify_view'),
]
