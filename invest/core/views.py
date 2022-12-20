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
# @api_view(['POST'])
def send_investissement(request):

    print(request.POST)
    url = "https://paytech.sn/api/payment/request-payment"
    ref_command = str(uuid.uuid4())
    payload = json.dumps({
        "item_name": f"invest/{request.user.investisseur.prenom} {request.user.investisseur.nom}",
        "item_price": int(request.POST.get("amount", None)),
        "currency": "XOF",
        "command_name": "Crowdlending Décembre 2022",
        "ref_command": ref_command,
        "env": "test",
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'API_KEY': API_KEY,
        'API_SECRET': API_SECRET
    }
    campagne = Campagne.objects.filter(
        libelle__iexact="Crowdlending Décembre 2022").first()
    response = requests.request("POST", url, headers=headers, data=payload)
    if campagne is not None:

        print(type(response))
        data = {
            "transaction_uid": ref_command,
            "investisseur": request.user.investisseur,
            "telephone": request.user.investisseur.telephone,
            "amount": request.POST.get("amount", None),
            "campagne": campagne,
            "type": request.POST.get("type_invest", None),
            "remboursement": request.POST.get("remboursement", None),
            "is_send": True,
            "status": "in_process"
        }
        investissement_form = InvestissementCreationForm(data)
        if investissement_form.is_valid:
            investissement_form.save()
    # print(response.json())

    return HttpResponse(json.dumps(response.json()))


@csrf_exempt
# @api_view(['POST'])
def ipn(request):
    if request.method == "POST":
        # # file_object = open(, 'a')
        # with open(BASE_DIR / 'test_log.txt', "a") as file_object:
        #     file_object.write(request.body)
        print(request.POST)

        # inputtxt = request.POST['getrow']
        api_key_sha256 = request.POST['api_key_sha256']
        api_secret_sha256 = request.POST['api_secret_sha256']
        my_api_secret_sha256 = hashlib.sha256(
            API_SECRET.encode('utf-8')).hexdigest()
        my_api_key_sha256 = hashlib.sha256(API_KEY.encode('utf-8')).hexdigest()
        # if my_api_key_sha256 == api_key_sha256 and my_api_secret_sha256 == api_secret_sha256:
        if request.POST["type_event"] and request.POST["type_event"] == "sale_complete":
            investissement = Investissement.objects.filter(
                transaction_uid=request.POST["ref_command"]).first()
            if investissement:
                investissement.status = "validate"
                investissement.save()
                echeance_calc(investissement)
            return HttpResponse(json.dumps({"message": "test", "status": 1}))
        elif request.POST["type_event"] and request.POST["type_event"] == "sale_canceled":
            investissement = Investissement.objects.filter(
                transaction_uid=request.POST["ref_command"]).first()
            if investissement:
                investissement.status = "cancelled"
                investissement.save()
            return HttpResponse(json.dumps({"message": "test", "status": 1}))
        else:
            return HttpResponse(json.dumps({"message": "test", "status": 0}))


@csrf_exempt
# @api_view(['POST'])
def success(request):
    # # response = json.loads(request.body)
    # investissement = Investissement.objects.filter(
    #     transaction_uid=request.POST.get("token", "")).first()
    # if investissement:
    #     investissement.status = "validate"
    #     investissement.save()
    # print(request.body)
    return render(request, "success.html")


@csrf_exempt
# @api_view(['POST'])
def cancel(request):
    # # response = json.loads(request.body)
    # investissement = Investissement.objects.filter(
    #     transaction_uid=request.POST.get("token", "")).first()
    # if investissement:
    #     investissement.status = "cancelled"
    #     investissement.save()
    # print(request.body)
    return render(request, "cancel.html")
