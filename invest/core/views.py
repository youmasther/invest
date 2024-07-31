from django.shortcuts import render
import requests
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http.response import HttpResponse
from .models import *
from .forms import *
from .helpers import echeance_calc
import json
import uuid
import hashlib
from invest.env import *

# Create your views here.


def home(request):
    campagne = Campagne.objects.first()
    context = {
        "campagne": campagne
    }
    return render(request, "index.html", context)


@csrf_exempt
def send_investissement(request):
    payload = {
        "item_name": f"invest/{request.user.investisseur.prenom} {request.user.investisseur.nom}",
        "item_price": int(request.POST.get("amount")),
        "currency": "XOF",
        "command_name": "Crowdlending Décembre 2022",
        "ref_command": str(uuid.uuid4()),
        "env": "test",
    }
    response = requests.post(
        "https://paytech.sn/api/payment/request-payment",
        json=payload,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "API_KEY": API_KEY,
            "API_SECRET": API_SECRET,
        },
    )

    if response.status_code == 200:
        campagne = Campagne.objects.filter(
            libelle__iexact="Crowdlending Décembre 2022"
        ).first()
        if campagne:
            Investissement.objects.create(
                transaction_uid=payload["ref_command"],
                investisseur=request.user.investisseur,
                telephone=request.user.investisseur.telephone,
                amount=request.POST.get("amount"),
                campagne=campagne,
                type=request.POST.get("type_invest"),
                remboursement=request.POST.get("remboursement"),
                is_send=True,
                status="in_process",
            )

    return HttpResponse(response.content, content_type="application/json")


@csrf_exempt
def ipn(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    api_key_sha256 = request.POST.get("api_key_sha256")
    api_secret_sha256 = request.POST.get("api_secret_sha256")
    if not (api_key_sha256 and api_secret_sha256):
        return HttpResponse(status=400)

    my_api_secret_sha256 = hashlib.sha256(
        API_SECRET.encode('utf-8')).hexdigest()
    my_api_key_sha256 = hashlib.sha256(API_KEY.encode('utf-8')).hexdigest()
    if api_key_sha256 != my_api_key_sha256 or api_secret_sha256 != my_api_secret_sha256:
        return HttpResponse(status=403)

    type_event = request.POST.get("type_event")
    if type_event == "sale_complete":
        investissement = Investissement.objects.filter(
            transaction_uid=request.POST.get("ref_command")).first()
        if investissement:
            investissement.status = "validate"
            investissement.save()
            echeance_calc(investissement)
            return HttpResponse(json.dumps({"message": "test", "status": 1}))
    elif type_event == "sale_canceled":
        investissement = Investissement.objects.filter(
            transaction_uid=request.POST.get("ref_command")).first()
        if investissement:
            investissement.status = "cancelled"
            investissement.save()
            return HttpResponse(json.dumps({"message": "test", "status": 1}))

    return HttpResponse(json.dumps({"message": "test", "status": 0}))


@csrf_exempt
def success(request):
    transaction_uid = request.POST.get("token", "")
    investissement = Investissement.objects.filter(transaction_uid=transaction_uid).first()
    if investissement:
        investissement.status = "validate"
        investissement.save(update_fields=['status'])
    return render(request, "success.html", content_type="text/html")


@csrf_exempt
def cancel(request):
    transaction_uid = request.POST.get("token", "")
    Investissement.objects.filter(transaction_uid=transaction_uid).update(status="cancelled")
    return render(request, "cancel.html")
