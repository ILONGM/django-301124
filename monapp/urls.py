from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),

    #create Urls for views displying portfolios & holdings
    path('portfolios/', views.list_portfolios, name='list_portfolios'),
    #path('portfolios/<int:portfolio_id>/', views.view_portfolio, name='view_portfolio'),
    path('action/', views.view_action, name='view_action'),
    path('portfolios/<int:portfolio_id>/', views.portfolio_detail, name='portfolio_detail'),

]