from django.db import models
from django.db.models import Sum

#table de portefeuille (si je gère plusieurs portefeuille)
class Portfolio(models.Model):
    name = models.CharField(max_length=100)         # Nom du portefeuille
    owner = models.CharField(max_length=100)        # Propriétaire du portefeuille
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

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

        # Retire les actions dont la quantité est zéro ou négative
        holdings = {k: v for k, v in holdings.items() if v > 0}

        return holdings

    # Cette fonction est a modifier car la formule pour le prix de vente ne marche pas.
    def holdings_with_cost(self):
        """
        Retourne les actions détenues avec leurs détails, incluant le coût total net.
        """
        holdings = self.holdings()  # Actions détenues (ticker et quantité)
        transactions = self.transaction_set.all()  # Transactions associées
        action_costs = {}

        for ticker, quantity_held in holdings.items():
            # Transactions d'achat et de vente pour cette action
            buy_transactions = transactions.filter(action__ticker=ticker, transaction_type='BUY')
            sell_transactions = transactions.filter(action__ticker=ticker, transaction_type='SELL')

            # Calcul du coût total des achats
            total_buy_cost = sum(buy.quantity * buy.price_per_share for buy in buy_transactions)

            # Calcul de la quantité vendue
            total_quantity_sold = sum(sell.quantity for sell in sell_transactions)

            # Ajuster le coût net pour tenir compte des ventes
            adjusted_cost = total_buy_cost * (quantity_held / (
                        quantity_held + total_quantity_sold)) if total_quantity_sold > 0 else total_buy_cost

            # Récupérer les détails de l'action
            action = buy_transactions.first().action if buy_transactions.exists() else None

            action_costs[ticker] = {
                'name': action.name if action else '',
                'ticker': ticker,
                'logo': action.logo if action and action.logo else '',
                'market': action.market if action else '',
                'shares': quantity_held,
                'net_cost': adjusted_cost
            }

        return action_costs

    def holdings_with_details(self):
        """
        Retourne les actions détenues avec leurs détails.
        """
        detailed_holdings = []
        action_details = self.holdings_with_cost()

        for ticker, details in action_details.items():
            logo_url = f'https://logo.clearbit.com/{details["name"]}.com'
            detailed_holdings.append({
                'name': details['name'],
                'ticker': ticker,
                'logo': logo_url,
                'market': details['market'],
                'shares': details['shares'],
                'net_cost': details['net_cost']
            })

        return detailed_holdings


    def __str__(self):
        return self.name



#tableau gérant les actions
class Action(models.Model):
    name = models.CharField(max_length=100)         # Nom de l'action (ex. Apple)
    ticker = models.CharField(max_length=10)        # Symbole boursier (ex. AAPL)
    logo = models.URLField(max_length=200, blank=True, null=True)  # URL du logo
    market = models.CharField(max_length=100)       # Marché (ex. NASDAQ)

    def save(self, *args, **kwargs):
        # Définit une URL par défaut si aucun logo n'est fourni
        if not self.logo:
            self.logo = f'https://logo.clearbit.com/{self.ticker.lower()}.com'
        super().save(*args, **kwargs)


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
