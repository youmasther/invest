from .models import Echeance
from .forms import EcheanceCreationForm
from dateutil.relativedelta import relativedelta


def echeance_calc(investissement):
    """
    docstring: cette fonction permet de 
    calculer et de créer les échéances d'un investissement
    """
    if investissement is None:
        print("investissement don't existe")
        return

    remboursement_mapping = {
        "Trimestriel": {
            "20%": quarterly_of_20_percent_for_6_months,
            "30%": quarterly_of_30_percent_for_1_year,
            "10%": quarterly_of_10_percent_for_1_year,
        },
        "Semestriel": {
            "20%": half_yearly_of_20_percent_for_6_months,
            "30%": half_yearly_of_30_percent_for_1_year,
            "10%": half_yearly_of_10_percent_for_1_year,
        },
        "Aterme": {
            "20%": once_of_20_percent_for_6_months,
            "30%": once_of_30_percent_for_1_year,
            "10%": once_of_10_percent_for_1_year,
        },
    }

    remboursement = investissement.remboursement
    type_ = investissement.type

    if remboursement not in remboursement_mapping or type_ not in remboursement_mapping[remboursement]:
        print("investissement case don't existe")
        return

    remboursement_mapping[remboursement][type_](investissement)


def quarterly_of_20_percent_for_6_months(investissement):
    montant_invest = investissement.amount // 2
    interet = montant_invest * 20 // 100
    total = montant_invest + interet
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=3*i)
        for i in range(2)
    ]
    EcheanceCreationForm.objects.bulk_create(
        EcheanceCreationForm(
            investissement=investissement,
            periode=periode,
            montant_investi=montant_invest,
            interet=interet,
            total=total,
            status='non',
        )
        for periode in periode_liste
    )
    print("quarterly_of_20_percent_for_6_months ok")


def quarterly_of_30_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=m)
        for m in (3, 6, 9, 12)
    ]
    montant_invest = investissement.amount // 4
    interet = montant_invest * 30 // 100
    total = montant_invest + interet
    EcheanceCreationForm.objects.bulk_create([
        EcheanceCreationForm(
            investissement=investissement,
            periode=periode,
            montant_investi=montant_invest,
            interet=interet,
            total=total,
            status='non',
        )
        for periode in periode_liste
    ])
    print("quarterly_of_30_percent_for_1_year ok")


def quarterly_of_10_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=m)
        for m in (3, 6, 9, 12)
    ]
    montant_invest = investissement.amount // 4
    interet = montant_invest * 10 // 100
    total = montant_invest + interet
    EcheanceCreationForm.objects.bulk_create([
        EcheanceCreationForm(
            investissement_id=investissement.id,
            periode=periode,
            montant_investi=montant_invest,
            interet=interet,
            total=total,
            status='non',
        )
        for periode in periode_liste
    ])
    print("quarterly_of_10_percent_for_1_year ok")


def half_yearly_of_20_percent_for_6_months(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+6)
    ] * len(periode_liste)
    montant_invest = investissement.amount
    interet = (montant_invest * 20) // 100
    total = montant_invest + interet
    EcheanceCreationForm.objects.bulk_create([
        EcheanceCreationForm(
            investissement=investissement,
            periode=periode,
            montant_investi=montant_invest,
            interet=interet,
            total=total,
            status='non',
        )
        for periode in periode_liste
    ])
    print("half_yearly_of_20_percent_for_6_months ok")


def half_yearly_of_30_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+6),
        investissement.campagne.fin_campagne + relativedelta(months=+12)
    ]
    montant_invest = investissement.amount // 2
    interet = (montant_invest * 30) // 100
    total = montant_invest + interet
    data = [
        {
            "investissement": investissement,
            "periode": periode,
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        for periode in periode_liste
    ]
    EcheanceCreationForm.objects.bulk_create(data)
    print("half_yearly_of_30_percent_for_1_year ok")


def half_yearly_of_10_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+6)
    ] * 2
    montant_invest = investissement.amount
    interet = (montant_invest * 10) // 100
    total = montant_invest + interet
    data = [
        {
            "investissement": investissement,
            "periode": periode,
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        for periode in periode_liste
    ]
    EcheanceCreationForm.objects.bulk_create(data)
    print("half_yearly_of_10_percent_for_1_year ok")


def once_of_20_percent_for_6_months(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+6)
    ]
    montant_invest, interet = investissement.amount, (investissement.amount * 20) // 100
    total = montant_invest + interet
    data = [
        {
            "investissement_id": investissement.id,
            "periode": periode,
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        for periode in periode_liste
    ]
    EcheanceCreationForm.objects.bulk_create(data, batch_size=1000)
    print("once_of_20_percent_for_6_months ok")


def once_of_30_percent_for_1_year(investissement):
    periode = investissement.campagne.fin_campagne + relativedelta(months=+12)
    montant_invest = investissement.amount
    interet = (montant_invest * 30) // 100
    total = montant_invest + interet
    EcheanceCreationForm.objects.create(
        investissement=investissement,
        periode=periode,
        montant_investi=montant_invest,
        interet=interet,
        total=total,
        status='non',
    )
    print("once_of_30_percent_for_1_year ok")


def once_of_10_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+12)
    ]
    montant_invest, interet = investissement.amount, (investissement.amount * 10) // 100
    total = montant_invest + interet
    EcheanceCreationForm.objects.bulk_create([
        EcheanceCreationForm(
            investissement=investissement,
            periode=periode,
            montant_investi=montant_invest,
            interet=interet,
            total=total,
            status='non',
        )
        for periode in periode_liste
    ])
    print("once_of_10_percent_for_1_year ok")
