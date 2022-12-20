from .models import Echeance
from .forms import EcheanceCreationForm
from dateutil.relativedelta import relativedelta


def echeance_calc(investissement):
    """
    docstring: cette fonction permet de 
    calculer et de créer les échéances d'un investissement
    """
    investissement_amount = 0
    if investissement is not None:
        if investissement.remboursement == "Trimestriel" and investissement.type == "20%":
            quarterly_of_20_percent_for_6_months(investissement)

        elif investissement.remboursement == "Trimestriel" and investissement.type == "30%":
            quarterly_of_30_percent_for_1_year(investissement)

        elif investissement.remboursement == "Trimestriel" and investissement.type == "10%":
            quarterly_of_10_percent_for_1_year(investissement)

        elif investissement.remboursement == "Semestriel" and investissement.type == "20%":
            half_yearly_of_20_percent_for_6_months(investissement)

        elif investissement.remboursement == "Semestriel" and investissement.type == "30%":
            half_yearly_of_30_percent_for_1_year(investissement)

        elif investissement.remboursement == "Semestriel" and investissement.type == "10%":
            half_yearly_of_10_percent_for_1_year(investissement)

        elif investissement.remboursement == "Aterme" and investissement.type == "20%":
            once_of_20_percent_for_6_months(investissement)

        elif investissement.remboursement == "Aterme" and investissement.type == "30%":
            once_of_30_percent_for_1_year(investissement)

        elif investissement.remboursement == "Aterme" and investissement.type == "10%":
            once_of_10_percent_for_1_year(investissement)

        else:
            print("investissement case don't existe")
    else:
        print("investissement don't existe")


def quarterly_of_20_percent_for_6_months(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+3),
        investissement.campagne.fin_campagne + relativedelta(months=+6)
    ]
    montant_invest = investissement.amount // 2
    interet = (montant_invest * 20) // 100
    total = montant_invest + interet
    for i in range(0, len(periode_liste)):
        data = {
            "investissement": investissement,
            "periode": periode_liste[i],
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        echeance_form = EcheanceCreationForm(data)
        if echeance_form.is_valid:
            echeance_form.save()
            print("quarterly_of_20_percent_for_6_months ok")
        else:
            print("quarterly_of_20_percent_for_6_months not ok")


def quarterly_of_30_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+3),
        investissement.campagne.fin_campagne + relativedelta(months=+6),
        investissement.campagne.fin_campagne + relativedelta(months=+9),
        investissement.campagne.fin_campagne + relativedelta(months=+12)
    ]
    montant_invest = investissement.amount // 4
    interet = (montant_invest * 30) // 100
    total = montant_invest + interet
    for i in range(0, len(periode_liste)):
        data = {
            "investissement": investissement,
            "periode": periode_liste[i],
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        echeance_form = EcheanceCreationForm(data)
        if echeance_form.is_valid:
            echeance_form.save()
            print("quarterly_of_30_percent_for_1_year ok")
        else:
            print("quarterly_of_30_percent_for_1_year not ok")


def quarterly_of_10_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+3),
        investissement.campagne.fin_campagne + relativedelta(months=+6),
        investissement.campagne.fin_campagne + relativedelta(months=+9),
        investissement.campagne.fin_campagne + relativedelta(months=+12)
    ]
    montant_invest = investissement.amount // 4
    interet = (montant_invest * 10) // 100
    total = montant_invest + interet
    for i in range(0, len(periode_liste)):
        data = {
            "investissement": investissement,
            "periode": periode_liste[i],
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        echeance_form = EcheanceCreationForm(data)
        if echeance_form.is_valid:
            echeance_form.save()
            print("quarterly_of_10_percent_for_1_year ok")
        else:
            print("quarterly_of_10_percent_for_1_year not ok")


def half_yearly_of_20_percent_for_6_months(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+6)
    ]
    montant_invest = investissement.amount
    interet = (montant_invest * 20) // 100
    total = montant_invest + interet
    for i in range(0, len(periode_liste)):
        data = {
            "investissement": investissement,
            "periode": periode_liste[i],
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        echeance_form = EcheanceCreationForm(data)
        if echeance_form.is_valid:
            echeance_form.save()
            print("half_yearly_of_20_percent_for_6_months ok")
        else:
            print("half_yearly_of_20_percent_for_6_months not ok")


def half_yearly_of_30_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+6),
        investissement.campagne.fin_campagne + relativedelta(months=+12)
    ]
    montant_invest = investissement.amount // 2
    interet = (montant_invest * 30) // 100
    total = montant_invest + interet
    for i in range(0, len(periode_liste)):
        data = {
            "investissement": investissement,
            "periode": periode_liste[i],
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        echeance_form = EcheanceCreationForm(data)
        if echeance_form.is_valid:
            echeance_form.save()
            print("half_yearly_of_30_percent_for_1_year ok")
        else:
            print("half_yearly_of_30_percent_for_1_year not ok")


def half_yearly_of_10_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+6)
    ]
    montant_invest = investissement.amount
    interet = (montant_invest * 10) // 100
    total = montant_invest + interet
    for i in range(0, len(periode_liste)):
        data = {
            "investissement": investissement,
            "periode": periode_liste[i],
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        echeance_form = EcheanceCreationForm(data)
        if echeance_form.is_valid:
            echeance_form.save()
            print("half_yearly_of_10_percent_for_1_year ok")
        else:
            print("half_yearly_of_10_percent_for_1_year not ok")


def once_of_20_percent_for_6_months(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+6)
    ]
    montant_invest = investissement.amount
    interet = (montant_invest * 20) // 100
    total = montant_invest + interet
    for i in range(0, len(periode_liste)):
        data = {
            "investissement": investissement,
            "periode": periode_liste[i],
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        echeance_form = EcheanceCreationForm(data)
        if echeance_form.is_valid:
            echeance_form.save()
            print("once_of_20_percent_for_6_months ok")
        else:
            print("once_of_20_percent_for_6_months not ok")


def once_of_30_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+12)
    ]
    montant_invest = investissement.amount
    interet = (montant_invest * 30) // 100
    total = montant_invest + interet
    for i in range(0, len(periode_liste)):
        data = {
            "investissement": investissement,
            "periode": periode_liste[i],
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        echeance_form = EcheanceCreationForm(data)
        if echeance_form.is_valid:
            echeance_form.save()
            print("once_of_30_percent_for_1_year ok")
        else:
            print("once_of_30_percent_for_1_year not ok")


def once_of_10_percent_for_1_year(investissement):
    periode_liste = [
        investissement.campagne.fin_campagne + relativedelta(months=+12)
    ]
    montant_invest = investissement.amount
    interet = (montant_invest * 10) // 100
    total = montant_invest + interet
    for i in range(0, len(periode_liste)):
        data = {
            "investissement": investissement,
            "periode": periode_liste[i],
            "montant_investi": montant_invest,
            "interet": interet,
            "total": total,
            "status": "non"
        }
        echeance_form = EcheanceCreationForm(data)
        if echeance_form.is_valid:
            echeance_form.save()
            print("once_of_10_percent_for_1_year ok")
        else:
            print("once_of_10_percent_for_1_year not ok")
