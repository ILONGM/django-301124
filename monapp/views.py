from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import TodoItem, Portfolio

# a views function takes a request and return a response
# views is a request handler


def home(request):
    return render(request,'index.html')

def todolist (request):
    todos = TodoItem.objects.all()
    return render(request, 'TodoItem.html', {'todos': todos})
# Create your views here.

# create a view that list portfolios
def list_portfolios(request):
    portfolios = Portfolio.objects.all()
    return render(request, 'list.html', {'portfolios': portfolios})

def view_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    holdings = portfolio.holdings()
    return render(request, 'detail.html', {'portfolio': portfolio, 'holdings': holdings})