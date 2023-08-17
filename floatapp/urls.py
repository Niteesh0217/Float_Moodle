from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout"),
    path('profile', views.profile, name="profile"),
    path('profile/edit', views.edit_profile, name="edit_profile"),
    path('profile/change-password', views.change_password, name="change-password"),
    path('profile/edit', views.edit_profile, name="edit_profile"),
    path('password_reset', views.reset_password, name="password_reset"),
    
]
    

