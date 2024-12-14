from django.contrib import admin
from .models import TodoItem, Portfolio, Action, Transaction, Dividend
# Register your models here.

admin.site.register(TodoItem)
admin.site.register(Portfolio)
admin.site.register(Action)
admin.site.register(Transaction)
admin.site.register(Dividend)

