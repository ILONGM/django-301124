from django.db import models

# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

#table de portefeuille (si je gère plusieurs portefeuille)
class Portfolio(models.Model):
    name = models.CharField(max_length=100)         # Nom du portefeuille
    owner = models.CharField(max_length=100)        # Propriétaire du portefeuille
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

#tableau gérant les actions
class Action(models.Model):
    name = models.CharField(max_length=100)         # Nom de l'action (ex. Apple)
    ticker = models.CharField(max_length=10)        # Symbole boursier (ex. AAPL)
    market = models.CharField(max_length=100)       # Marché (ex. NASDAQ)
    sector = models.CharField(max_length=100)       # Secteur (ex. Technologie)
    description = models.TextField(blank=True)      # Description de l'action
    created_at = models.DateTimeField(auto_now_add=True)  # Date d'ajout


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
    notes = models.TextField(blank=True)


class Dividend(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)  # Lien vers l'action
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)  # Portefeuille associé
    amount = models.FloatField()                                   # Montant total du dividende
    dividend_date = models.DateTimeField()                         # Date du paiement
