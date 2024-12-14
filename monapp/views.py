from django.shortcuts import render, HttpResponse
from .models import TodoItem

# a views function takes a request and return a response
# views is a request handler


def home(request):
    return render(request,'index.html')

def todolist (request):
    todos = TodoItem.objects.all()
    return render(request, 'TodoItem.html', {'todos': todos})
# Create your views here.
