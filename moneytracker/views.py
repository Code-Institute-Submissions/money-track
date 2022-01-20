from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    return render(request, 'expenses/index.html')


@login_required(login_url='/authentication/login')
def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expenses.html', context)

    if request.method == 'GET':
        return render(request, 'expenses/add_expenses.html', context)
