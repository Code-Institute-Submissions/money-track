from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, UserSalary
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

def search_salary(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        salary = UserSalary.objects.filter(amount__istartswith=search_str, owner=request.user) | UserSalary.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserSalary.objects.filter(
            description__icontains=search_str, owner=request.user) | UserSalary().objects.filter(
            category__istartswith=search_str, owner=request.user)
        data = salary.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Source.objects.all()
    salary = UserSalary.objects.filter(owner=request.user)
    paginator = Paginator(salary, 5)
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)

    context = {
        'salary': salary,
        'page_object': page_object
    }
    return render(request, 'salary/salary.html', context)


@login_required(login_url='/authentication/login')
def add_salary(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'salary/add_salary.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'salary/add_salary.html', context)
        description = request.POST['description']
        date = request.POST['salary_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'salary/add_salary.html', context)

        UserSalary.objects.create(owner=request.user, amount=amount,
                               date=date, source=source, description=description)

        messages.success(request, 'Salary saved successfully')

        return redirect('salary')


def salary_edit(request, id):
    sources = Source.objects.all()
    salary = UserSalary.objects.get(pk=id)
    context = {
        'salary': salary,
        'values': salary,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-salary.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'salary/edit-salary.html', context)
        description = request.POST['description']
        date = request.POST['salary_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'salary/edit-salary.html', context)

        salary.owner = request.user
        salary.amount = amount
        salary.date = date
        salary.source = source
        salary.description = description

        salary.save()
        messages.success(request, 'Salary updated successfully')

        return redirect('salary')


def delete_salary(request, id):
    salary = UserSalary.objects.get(pk=id)
    salary.delete()
    messages.success(request, 'Salary deleted successfully')
    return redirect('salary')