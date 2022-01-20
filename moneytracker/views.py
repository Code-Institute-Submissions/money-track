from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)

    context = {
        'expenses': expenses
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expenses(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expenses.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expenses.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expenses.html', context)

        Expense.objects.create(owner=request.user, amount=amount,
                               date=date, category=category, description=description)

        messages.success(request, 'Expense saved successfully')

        return redirect('moneytracker')


def expense_edit(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category 
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated successfully')

        return redirect('moneytracker')
