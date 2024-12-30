from django.contrib import admin
from .models import Portfolio, Action, Transaction, Dividend
# Register your models here.

admin.site.register(Portfolio)
admin.site.register(Action)
admin.site.register(Dividend)

