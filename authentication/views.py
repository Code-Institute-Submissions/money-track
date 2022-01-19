from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User


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

