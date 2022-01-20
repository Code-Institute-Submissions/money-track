from .views import Registration, UsernameValidation, EmailValidation, LogIn
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('registration', Registration.as_view(), name="registration"),
    path('login', LogIn.as_view(), name="login"),
    path('authenticate-username', csrf_exempt(UsernameValidation.as_view()),
         name="authenticate-username"),
    path('authenticate-email', csrf_exempt(EmailValidation.as_view()), name="authenticate-email")
]
