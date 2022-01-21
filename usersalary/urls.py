from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name = "moneytracker"),
    path('add-salary', views.add_salary, name = "add-salary"),
    path('edit-salary/<int:id>', views.salary_edit, name = "salary-edit"),
    path('salary-delete/<int:id>', views.delete_salary, name = "salary-delete"),
    path('search-salary', csrf_exempt(views.search_salary), name= "search_salary")
]


