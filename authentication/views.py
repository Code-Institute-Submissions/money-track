from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from email_validator import validate_email,  EmailNotValidError
from django.contrib import messages
from django.contrib import auth



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

        # GET DATA
        # VALIDATE
        # CREATE USER ACCOUNT

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email). exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short!')
                    return render(request, 'authentication/registration.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Registration Success!')
                return render(request, 'authentication/registration.html')

        return render(request, 'authentication/registration.html')

class LogIn(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome ' + user.username + ' you are now logged in')

                    return redirect('moneytracker')

            messages.error(request, 'Invalid credentials, please try again')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')

class LogOut(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out successfully')
        return redirect('login')


