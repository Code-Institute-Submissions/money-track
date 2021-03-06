from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class UserSalary(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.CharField(max_length=200)

    def __str__(self):
        return self.source

    class Meta:
        ordering: ['-date']
        verbose_name_plural = 'User Salaries'

class Source(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    