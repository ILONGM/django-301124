from django.db import models
from django.db.models import Sum



#table de portefeuille (si je gère plusieurs portefeuille)
class Portfolio(models.Model):
    name = models.CharField(max_length=100)         # Nom du portefeuille
    owner = models.CharField(max_length=100)        # Propriétaire du portefeuille
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    # Il fau créer une méthode pour calculer le nombre d'actions détenus dans un portefeuille
    def holdings(self):
        """
        Calcule et retourne les actions détenues dans ce portefeuille.
        Le résultat est un dictionnaire où les clés sont les tickers des actions
        et les valeurs sont les quantités détenues.
        """
        holdings = {}
        transactions = self.transaction_set.all()

        for transaction in transactions:
            if transaction.action.ticker not in holdings:
                holdings[transaction.action.ticker] = 0

            if transaction.transaction_type == 'BUY':
                holdings[transaction.action.ticker] += transaction.quantity
            elif transaction.transaction_type == 'SELL':
                holdings[transaction.action.ticker] -= transaction.quantity

        # Retirer les actions dont la quantité est zéro ou négative
        holdings = {k: v for k, v in holdings.items() if v > 0}

        return holdings

    def holdings_with_details(self):
        """
        Retourne les actions détenues avec leurs détails.
        """
        holdings = self.holdings()
        actions = Action.objects.filter(ticker__in=holdings.keys())
        detailed_holdings = []

        for action in actions:
            detailed_holdings.append({
                'name': action.name,
                'ticker': action.ticker,
                'logo': f'https://logo.clearbit.com/{action.name.lower()}.com',
                'market': action.market,
                'shares': holdings[action.ticker],
            })

        return detailed_holdings


    def __str__(self):
        return self.name



#tableau gérant les actions
class Action(models.Model):
    name = models.CharField(max_length=100)         # Nom de l'action (ex. Apple)
    ticker = models.CharField(max_length=10)        # Symbole boursier (ex. AAPL)
    logo = f'https://logo.clearbit.com/{name}.com'
    market = models.CharField(max_length=100)       # Marché (ex. NASDAQ)

#Table de log des transactions
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('BUY', 'Achat'),
        ('SELL', 'Vente'),
        ('DIV', 'Dividende'),
    ]
    action = models.ForeignKey(Action, on_delete=models.CASCADE)  # Lien vers l'action concernée
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)  # Portefeuille associé
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)  # Type de transaction
    quantity = models.PositiveIntegerField()                     # Quantité d'actions
    price_per_share = models.FloatField()                        # Prix unitaire
    transaction_date = models.DateTimeField()                    # Date de la transaction
















class Dividend(models.Model):
     action = models.ForeignKey(Action, on_delete=models.CASCADE)  # Lien vers l'action
     portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)  # Portefeuille associé
     amount = models.FloatField()                                   # Montant total du dividend     dividend_date = models.DateTimeField()                         # Date du paiement
