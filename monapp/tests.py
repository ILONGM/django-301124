from django.db.models.expressions import result
from django.test import TestCase

from monapp.models import Portfolio, Action, Transaction

class ModelsPortfolioTest(TestCase):
    def setUp(self):
        # Set up un portefeuille test
        self.instance = Portfolio.objects.create(name = "portfolio_test", owner = "mathieu", created_at="Dec2024")

        # Set up deux actions pour le test
        self.action1 = Action.objects.create(name="Apple", ticker="AAPL", market="NASDAQ")
        self.action2 = Action.objects.create(name="Tesla", ticker="TSLA", market="NASDAQ")

        # Ajoute des transactions au portefeuille test
        Transaction.objects.create(
            action=self.action1,
            portfolio=self.instance,
            transaction_type="BUY",
            quantity=10,
            price_per_share=150.00,
            transaction_date="2023-12-01"
        )
        Transaction.objects.create(
            action=self.action1,
            portfolio=self.instance,
            transaction_type="SELL",
            quantity=5,
            price_per_share=160.00,
            transaction_date="2023-12-02"
        )
        Transaction.objects.create(
            action=self.action2,
            portfolio=self.instance,
            transaction_type="BUY",
            quantity=69,
            price_per_share=420.00,
            transaction_date="2023-12-01"
        )

    def test_holdings(self):
        # Appelle la méthode holdings et teste le résultat
        result = self.instance.holdings()
        print(result)


    def test_holdings_with_cost(self):
        result = self.instance.holdings_with_cost()
        #print(result)

    def test_holdings_with_details(self):
        result = self.instance.holdings_with_details()
        #print(result)


    def test_total_invested(self):
        result = self.instance.total_invested()
        print(result)
# Create your tests here.
