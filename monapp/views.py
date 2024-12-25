from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Portfolio, Action


# a views function takes a request and return a response
# views is a request handler


def home(request):
    return render(request,'index.html')


# create a view that list portfolios
def list_portfolios(request):
    portfolios = Portfolio.objects.all()
    return render(request, 'list.html', {'portfolios': portfolios})


def view_action(request):
    listaction = Action.objects.values()
    return HttpResponse(listaction)


#Création d'une vue pour renvoyer une vision détaillée du portefeuille
def portfolio_detail(request, portfolio_id):
    try:
        portfolio = Portfolio.objects.get(pk=portfolio_id)
        holdings = portfolio.holdings_with_details()

        # Ajout d'un prix fictif (remplacez-le par un appel API si nécessaire)
        for holding in holdings:
            holding['currentPrice'] = 100.0  # Prix fictif
            holding['totalValue'] = holding['shares'] * holding['currentPrice']

        return JsonResponse({'portfolios': holdings})
    except Portfolio.DoesNotExist:
        return JsonResponse({'error': 'Portfolio not found'}, status=404)
