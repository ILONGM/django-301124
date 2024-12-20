from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("todo/",views.todolist,name="bdd"),

    #create Urls for views displying portfolios & holdings
    path('portfolios/', views.list_portfolios, name='list_portfolios'),
    path('portfolios/<int:portfolio_id>/', views.view_portfolio, name='view_portfolio'),
]