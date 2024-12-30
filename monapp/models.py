from django.contrib import admin
from django.db import models
from django.db.models import Sum

#table de portefeuille (si je gère plusieurs portefeuille)
class Portfolio(models.Model):
    name = models.CharField(max_length=100)         # Nom du portefeuille
    owner = models.CharField(max_length=100)        # Propriétaire du portefeuille
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def holdings(self):
        """
        Calcule et retourne le nombre d'actions détenues dans ce portefeuille.
        Le résultat est un dictionnaire où les clés sont les tickers des actions
        et les valeurs sont les quantités détenues.
        Gère les achat et les ventes
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

    def portfolio_data_analysis(self):
        """Calcul le PRU et d'autres indicateurs de performance"""
        holdings = self.holdings()
        transactions = self.transaction_set.all()
        total_historically_invested = {}

        # calcule le total buy en Eur et # et retourne un PRU
        for ticker, quantity_held in holdings.items():
            buy_transactions = transactions.filter(action__ticker=ticker, transaction_type = 'BUY')
            sell_transactions = transactions.filter(action__ticker=ticker, transaction_type= 'SELL')
            #inclure les dividendes ici?

            #récupération des détails des actions (noms, logo etc)
            action = buy_transactions.first().action if buy_transactions.exists() else None

            #calcul des montants investis et du PRU
            quantity_bought = sum(buy.quantity for buy in buy_transactions)
            total_paid = sum(buy.quantity*buy.price_per_share for buy in buy_transactions)
            averaged_price_paid = total_paid/quantity_bought
            current_invested_at_cost = quantity_held * averaged_price_paid

            #calcul des gains réalisés
            quantity_sold = sum(sell.quantity for sell in sell_transactions)
            total_sold = sum(sell.quantity*sell.price_per_share for sell in sell_transactions)
            profit_realised = total_sold - (quantity_sold * averaged_price_paid)


            total_historically_invested [ticker] = {
                'name': action.name if action else '',
                'ticker' : ticker,
                'market': action.market if action else '',
                'quantity_bought' : quantity_bought,
                'quantity_sold' : quantity_sold,
                'shares' : quantity_held,
                'total_invested' : total_paid,
                'total_sold':total_sold,
                'PRU' : averaged_price_paid,
                'current_invested_at_cost' : current_invested_at_cost,
                'profit_realised' : profit_realised,
            }
        return total_historically_invested

    #def realised_gainloss(self):

    def holdings_with_details(self):
        """
        Retourne les actions détenues avec leurs détails. Ajoute le logo
        """
        detailed_holdings = []
        action_details = self.portfolio_data_analysis()

        for ticker, details in action_details.items():
            logo_url = f'https://logo.clearbit.com/{details["name"]}.com'
            detailed_holdings.append({
                'name': details['name'],
                'ticker': ticker,
                'logo': logo_url,
                'market': details['market'],
                'shares': details['shares'],
                'total_invested': details['total_invested'],
                'current_invested_at_cost': details['current_invested_at_cost'],
                'PRU':details['PRU'],
                'total_sold':details['total_sold'],
                'profit_realised' : details['profit_realised'],
            })

        return detailed_holdings


    def __str__(self):
        return self.name



class Action(models.Model):
    name = models.CharField(max_length=100)         # Nom de l'action (ex. Apple)
    ticker = models.CharField(max_length=10)        # Symbole boursier (ex. AAPL)
    logo = f'https://logo.clearbit.com/{name}.com'
    market = models.CharField(max_length=100)       # Marché (ex. NASDAQ)

    def __str__(self):
        return self.name

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

# exempl de comment utiliser le string pour afficher dans ladmin
    def __str__(self):
        return f'{self.transaction_date.strftime("%Y-%m-%d")} - {self.transaction_type} - {self.quantity}-{self.action.ticker}'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'action',
        'portfolio',
        'transaction_date',
        'transaction_type',
        'quantity'
    )

    list_filter = [
        'transaction_type'
    ]










class Dividend(models.Model):
     action = models.ForeignKey(Action, on_delete=models.CASCADE)  # Lien vers l'action
     portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)  # Portefeuille associé
     amount = models.FloatField()                                   # Montant total du dividend     dividend_date = models.DateTimeField()                         # Date du paiement
