from django import forms
from .models import *


class CampagneCreationForm(forms.ModelForm):

    class Meta:
        model = Campagne
        fields = ('libelle', 'status', 'send_date',
                  'users')


class InvestissementCreationForm(forms.ModelForm):

    class Meta:
        model = Investissement
        fields = ('transaction_uid', 'investisseur', 'telephone', 'amount',
                  'campagne', 'operateur', "type", "remboursement", 'is_send', 'status')