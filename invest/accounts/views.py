from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser as User
from django.http.response import HttpResponse
from .forms import *
from core.models import Investissement, Echeance
import json
import os

# Create your views here.


def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.POST:
        email = request.POST.get(
            'email', '') if 'email' in request.POST else None
        password = request.POST.get(
            'password', '') if 'password' in request.POST else None
        user = auth.authenticate(email=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'index.html', {'error': 'Login ou mot de passe incorrect'})
    else:
        return render(request, 'index.html', {'message': ''})


def logout(request):
    if request.method == "GET":
        print("logout")
        auth.logout(request)
        return redirect('home')


def register(request):
    if request.method == 'POST':
        user = None
        data = {
            'email': request.POST.get('email', ''),
            'password1': request.POST.get('password1', ''),
            'password2': request.POST.get('password2', ''),
        }
        data2 = {
            'prenom': request.POST.get('prenom', ''),
            'nom': request.POST.get('nom', ''),

        }
        if User.objects.filter(email=data["email"]).first() is not None:
            return HttpResponse(json.dumps({"message": "Un utilisateur avec ce email exite déja", "status": 0}))

        user_form = UserCreationForm2(data)
        if user_form.is_valid():
            user_form.save()
            user = User.objects.filter(email=data["email"]).first()
        else:
            return HttpResponse(json.dumps({"message": "Erreur:Veuillez revoir les informations soumisent", "status": 0}))

        data2 = {
            'prenom': request.POST.get('prenom', ''),
            'nom': request.POST.get('nom', ''),
            "telephone": f"{request.POST.get('indicatif', '')}{request.POST.get('phone', '')} ",
            # "adresse": f"{request.POST.get('pays', '')}, {request.POST.get('adresse', '')} ",
            # "cni": request.POST.get('cni', ''),
            'user': user
        }

        investisseur_form = InvestisseurForm(data2)
        if investisseur_form.is_valid:
            investisseur_form.save()
            return HttpResponse(json.dumps({"message": "Votre compte a été bien créé", "status": 1}))
        else:
            user.delete()
            return HttpResponse(json.dumps({"message": "Erreur:Veuillez revoir les informations soumisent", "status": 0}))
    else:
        return render(request, 'register.html')
# @login_required(login_url='/')


@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeFormEdit(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Votre mot de passe a été modifier avec succés')
            return redirect('change_password')
        else:
            messages.error(
                request, 'SVP veillez corriger les erreurs ci aprés.')
    else:
        form = PasswordChangeFormEdit(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@login_required(login_url='/')
def profile(request):
    investisseur = request.user.investisseur
    investissements = Investissement.objects.filter(
        investisseur=request.user.investisseur)

    return render(request, "profile.html", {"investisseur": investisseur, "investissements": list(reversed(investissements))})


def hx_update_user_profile_img(request):
    if request.method == 'POST':
        if request.user.profile_image:
            try:
                os.remove(os.path.abspath(request.user.profile_image.url))
            except Exception as e:
                print('Exception in removing old profile image: ', e)
        print(request.FILES)
        profile_image_form = ProfileImageUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if profile_image_form.is_valid():
            profile_image_form.save()
            print("ok")
            return HttpResponse(json.dumps({"message": "Photo de profil changer avec succes", "status": 1}))
        else:
            return HttpResponse(json.dumps({"message": "Erreur:Veuillez revoir les informations soumisent", "status": 0}))


def hx_update_user_carte_img(request):
    if request.method == 'POST':
        if request.user.profile_image:
            try:
                os.remove(os.path.abspath(request.user.investisseur.carte.url))
            except Exception as e:
                print('Exception in removing old profile image: ', e)
        carte_form = CarteImageUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if carte_form.is_valid():
            print("Ok carte")
            carte_form.save()
            return HttpResponse(json.dumps({"message": "Piéce changer avec succes", "status": 1}))
        else:
            return HttpResponse(json.dumps({"message": "Erreur:Veuillez revoir les informations soumisent", "status": 0}))
