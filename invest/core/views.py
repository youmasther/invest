from django.shortcuts import render
import requests
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http.response import HttpResponse
import json
import uuid

# Create your views here.


def home(request):
    print(f"test:{request.scheme}://{request.META['HTTP_HOST']}")
    return render(request, "index.html", {})


@csrf_exempt
# @api_view(['POST'])
def send_investissement(request):
    paymentRequestUrl = "https://paytech.sn/api/payment/request-payment"
    params = {
        "item_name": "Iphone 7",
        "item_price": "100",
        "currency": "XOF",
        "ref_command": str(uuid.uuid4()),
        "command_name": "Paiement Iphone 7 Gold via PayTech",
        "env": "test",
        "ipn_url": f"{request.scheme}://{request.META['HTTP_HOST']}/api/ipn",
        "success_url": f"{request.scheme}://{request.META['HTTP_HOST']}/api/success",
        "cancel_url": f"{request.scheme}://{request.META['HTTP_HOST']}/api/cancel",
        "custom_field": {
            "custom_fiel1": "value_1",
            "custom_fiel2": "value_2"
        }
    }

    headers = {
        "Accept": "application/json",
        'Content-Type': "application/json",
        "API_KEY": "cd31e5f124dec13f236f171368bc8036ffd8314c35f86dfc4b02098f4c41a661",
        "API_SECRET": "37f76ec46a6a567fd0f85e08e0b59a53b34d91140dbbff1c15a1e78d48802d0b"
    }

    r = requests.post(paymentRequestUrl,
                      data=json.dumps(params), headers=headers)
    print(r.text)

    return HttpResponse(json.dumps({"message": "test", "status": 0}))


def ipn(request):
    pass
