from django.contrib import admin
from .models import *

# Register your models here.


class CampagneAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'libelle', 'users',
                    'status', 'make_at')
    list_display_links = ('__str__', 'libelle',)
    list_filter = ('users',)
    # readonly_fields=('slug',)
    search_fields = ('libelle', 'users', 'status',)
    list_per_page = 25


class InvestissementAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'transaction_uid', 'campagne', 'investisseur',
                    'telephone', 'amount', 'status', 'is_send', 'make_at')
    list_display_links = ('campagne', 'transaction_uid',)
    search_fields = ('campagne', 'transaction_uid', 'amount',)


@admin.register(Echeance)
class EcheanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'periode', 'montant_investi', 'interet',
                    'total', 'status', 'date_remboursement')
    list_display_links = ('__str__', 'periode',)
    search_fields = ('periode',)


admin.site.register(Campagne, CampagneAdmin)
admin.site.register(Investissement, InvestissementAdmin)

# admin.site.register(Commission, CommissionAdmin)
# admin.site.register(Operator, OperatorAdmin)
