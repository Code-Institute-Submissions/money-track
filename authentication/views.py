from django.shortcuts import render
from django.views import View



class Registration(View):
    def get(self, request):
        return render(request, 'authentication/registration.html')

