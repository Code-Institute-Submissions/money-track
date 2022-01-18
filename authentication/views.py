from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse


class UsernameAuthentication(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric characters.'}, status=400)

        return JsonResponse({'Username Valid!': True})


class Registration(View):
    def get(self, request):
        return render(request, 'authentication/registration.html')

