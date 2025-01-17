from django.db import models
from accounts.models import CustomUser, Investisseur

# Create your models here.


class Campagne(models.Model):
    STATUS_TYPE_CHOICES = (('in_process', 'EN COURS'),
                           ('ended', 'TERMINER'), ('cancelled', 'ANNULER'))
    libelle = models.CharField(max_length=100, null=True)
    amount_needed = models.IntegerField(null=True)
    debut_campagne = models.DateField(null=True)
    fin_campagne = models.DateField(null=True)
    status = models.CharField(
        max_length=100, choices=STATUS_TYPE_CHOICES, default="in_process")
    make_at = models.DateTimeField(auto_now_add=True)
    users = models.ForeignKey(CustomUser, blank=True,
                              null=True, on_delete=models.SET_NULL)
    is_over = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Campagne"
        verbose_name_plural = "Campagnes"
        db_table = "campagne"

    def __str__(self) -> str:
        return f'{self.libelle}'

    @property
    def investissements(self):
        return Investissement.objects.filter(campagne=self)

    @property
    def nb_investissements(self):
        return Investissement.objects.filter(campagne=self).count()

    @property
    def nb_investissements_valid(self):
        return Investissement.objects.filter(campagne=self, status="validate").count()

    @property
    def investissements_in_process(self):
        return Investissement.objects.filter(campagne=self, status="in_process", is_send=False)

    @property
    def solde_obtenu(self):
        transactions = Investissement.objects.filter(
            campagne=self, status="validate")
        somme = 0
        if transactions:
            somme = sum(int(transaction.amount)
                        for transaction in transactions)
        if somme == 0:
            return 0
        return somme

    @property
    def pourcentage(self):
        total = self.solde_obtenu
        if total == 0:
            return 0
        return (int(total) * 100) // int(total)

# class Operator(models.Model):
#     OPERATOR_TYPE_CHOICES = (('wallet', 'Wallet'), ('visa', 'VISA'))
#     name = models.CharField(max_length=100)
#     type = models.CharField(
#         max_length=100, choices=OPERATOR_TYPE_CHOICES, default="wallet")
#     code = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


class Investissement(models.Model):
    TYPE_REMBOURSEMENT_CHOICES = (
        ('Trimestriel', 'Trimestriel'), ('Semestriel', 'Semestriel'), ('Aterme', 'A terme(Annuel)'))
    STATUS_TYPE_CHOICES = (('in_process', 'EN COURS'),
                           ('validate', 'VALIDER'), ('cancelled', 'ANNULER'))
    TYPE_INVESTISSEMENT_CHOICES = (
        ('20%', '20% pour 6 mois'), ('30%', '30% pour 12 mois'), ('10%', 'credite mon compte subito'))
    transaction_uid = models.CharField(max_length=100, unique=True)
    investisseur = models.ForeignKey(Investisseur, on_delete=models.CASCADE)
    amount = models.IntegerField()
    telephone = models.CharField(max_length=100, null=True, blank=True)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)

    is_send = models.BooleanField(default=False)
    operateur = models.CharField(max_length=10, default='OM')
    type = models.CharField(max_length=100, choices=TYPE_INVESTISSEMENT_CHOICES,
                            default=TYPE_INVESTISSEMENT_CHOICES[0][0], null=True)
    remboursement = models.CharField(
        max_length=100, choices=TYPE_REMBOURSEMENT_CHOICES, default=TYPE_REMBOURSEMENT_CHOICES[0][0], null=True)
    status = models.CharField(
        max_length=100, choices=STATUS_TYPE_CHOICES, default="in_process")
    make_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Investissement"
        verbose_name_plural = "Investissements"
        db_table = "investissement"

    def __str__(self) -> str:
        return f'{self.campagne}/{self.investisseur}'

    @property
    def echeances(self):
        echeances = Echeance.objects.filter(investissement=self)
        if echeances:
            return echeances
        else:
            return None


class Echeance(models.Model):
    STATUS_TYPE_CHOICES = (('yes', 'Rembourser'),
                           ('non', 'Non Rembourser'))
    investissement = models.ForeignKey(
        Investissement, on_delete=models.CASCADE)
    periode = models.DateField()
    montant_investi = models.IntegerField(default=0)
    interet = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    status = status = models.CharField(
        max_length=100, choices=STATUS_TYPE_CHOICES, default="non")
    date_remboursement = models.DateTimeField(
        verbose_name="dernier modification", auto_now=True)

    class Meta:
        verbose_name = "Echeance"
        verbose_name_plural = "Echeances"
        db_table = "echeance"

    def __str__(self) -> str:
        return f'{self.investissement} '
