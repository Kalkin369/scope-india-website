# urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('registration/',views.registration, name='registration'),
    path('register/', views.registration_view, name='registration_view'),
    path('verify/<str:token>/', views.verify_email, name='verify_email'),
    path('courses/<slug:slug>/',views.course_detail,name='course_detail'),
    path('login/',views.login_view, name='login_view'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view, name='logout_view'),
    path('reset_temp_password/',views.reset_temp_password,name='reset_temp_password'),
    path('forgot_password/',views.forgot_password_view,name='forgot_password'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('course_signup/',views.course_signup_view,name='course_signup_view'),
    path('profiledit/',views.profile_edit_view,name='profile_edit_view'),
    path('password/change/', auth_views.PasswordChangeView.as_view(
        template_name='myapp/password_change.html',
        success_url='/password/change/done/'
    ), name='password_change'),

    path('password/change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='myapp/password_change_done.html'
    ), name='password_change_done'),
]

