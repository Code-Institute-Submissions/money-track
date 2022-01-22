from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
import datetime
import csv
import xlsxwriter
import xlwt


def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__istartswith=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_object = Paginator.get_page(paginator, page_number)

    context = {
        'expenses': expenses,
        'page_object': page_object
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


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted successfully')
    return redirect('moneytracker')


def expense_category_summary(request):
    current_date = datetime.date.today()
    three_months_ago = current_date-datetime.timedelta(days=30*3)
    expenses = Expense.objects.filter(owner=request.user, date__gte=three_months_ago, date__lte=current_date)
    summary = {}

    def get_expense_category(expense):
        return expense.category
    category_list = list(set(map(get_expense_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount

        return amount

    for x in expenses:
        for y in category_list:
            summary[y] = get_expense_category_amount(y)

    return JsonResponse({ 'expense_category_data': summary }, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')


def salary_category_summary(request):
    current_date = datetime.date.today()
    three_months_ago = current_date-datetime.timedelta(days=30*3)
    salary = UserSalary.objects.filter(owner=request.user, date__gte=three_months_ago, date__lte=current_date)
    summary = {}

    def get_salary_category(salary):
        return salary.category
    category_list = list(set(map(get_salary_category, salary)))

    def get_salary_category_amount(category):
        amount = 0
        filtered_by_category = salary.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount

        return amount

    for x in salary:
        for y in category_list:
            summary[y] = get_salary_category_amount(y)

    return JsonResponse({ 'salary_category_data': summary }, safe=False)



def salary_stats_view(request):
    return render(request, 'salary/salary_stats.html')


def export_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response


def export_excel(request):
    reply = HttpResponse(content_type='application/ms-excel')
    reply['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.xls'

    wbook = xlwt.Workbook(encoding='utf-8')
    wsheet = wbook.add_sheet('Expenses')

    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']

    for col_num in range(len(columns)):
        wsheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Expense.objects.filter(owner=request.user).values_list('amount', 'description', 'category', 'date')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            wsheet.write(row_num, col_num, str(row[col_num]), font_style)

    wbook.save(reply)

    return reply


def export_pdf(request):

    respond = HttpResponse(content_type='application/pdf')
    repond['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.pdf'






