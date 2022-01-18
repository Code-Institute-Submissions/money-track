from .views import Registration
from django.urls import path


urlpatterns = [
    path('registration', Registration.as_view(), name="registration"),
    path('authenticate-username', UsernameAuthentication.as_view,
         name="authenticate-username")
]
