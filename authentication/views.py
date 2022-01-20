from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from email_validator import validate_email,  EmailNotValidError
from django.contrib import messages



class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry! Email already in use, please choose another one.'}, status=409)
        return JsonResponse({'Email Valid!': True})

class UsernameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain numbers and letters.'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry! Username already in use, please choose another one.'}, status=409)
        return JsonResponse({'Username Valid!': True})


class Registration(View):
    def get(self, request):
        return render(request, 'authentication/registration.html')

    def post(self, request):
        messages.success(request, 'Success!')
        messages.warning(request, 'Warning!')
        messages.info(request, 'Info!')
        messages.error(request, 'Error!')
        return render(request, 'authentication/registration.html')

