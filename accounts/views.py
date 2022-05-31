import re
import json
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, Http404
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import LoginForm, RegistrationForm, UserAddressForm
from .models import EmailConfirmed, UserDefaultAddress


def logout_view(request):
    print("log out")
    logout(request)
    messages.success(request, "Successfully logout. Come Back Soon", extra_tags='safe')
    return HttpResponseRedirect('/')



def login_view(request):
    form = LoginForm(request.POST or None)
    btn = "login"
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Successfully Login. keep Shopping")
        return HttpResponseRedirect('/')
        #user.emailconfirmed.activate_user_email()
    
    context = {
        'form': form,
        'submit_btn': btn,
    }
    
    return render(request, "form.html", context)



def registration_view(request):
    form = RegistrationForm(request.POST or None)
    btn = "join"
    if form.is_valid():
        new_user = form.save(commit=False)
        #new_user.first_name = "joy" here to do stuff with model
        new_user.save()
        messages.success(request, "Successfully Register. please Check Your Email for Confermation")
        return HttpResponseRedirect('/')
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # user = authenticate(username= username, password= password)
        # login(request, user)
    
    context = {
        'form': form,
        'submit_btn': btn,
    }

    return render(request, "form.html", context)



SHA1_RE = re.compile('^[a-f0-9]{40}$')


def activation_view(request, activation_key):
    #return HttpResponseRedirect('/')
    if SHA1_RE.search(activation_key):
        print("activation complete")
        try:
            instance = EmailConfirmed.objects.get(activation_key=activation_key)
        except EmailConfirmed.DoesNotExist:
            instance = None
            messages.success(request, "Error found in yout request")
            return HttpResponseRedirect('/')
            #raise Http404
        if instance is not None and not instance.confirmed:
            page_message = "confirmation successfull ! welcome"
            instance.confirmed=True
            instance.activation_key = "confirmed"
            instance.save()
            messages.success(request, "Successfully confirmed. keep shopping")
        elif instance is not None and instance.confirmed:
            page_message ="Allready confermed"
            messages.success(request, "Alredy confirmed. keep shopping")
        else:
            page_message=""
            
        context = {"page_message": page_message}
        return render(request, "accounts/activation_complete.html", context)
    else:
        raise Http404
   

def add_user_address(request):
    print(request.GET)
    try:
        next_page = request.GET.get("next")
    except:
        next_page = None
    if request.method == "POST":
        form = UserAddressForm(request.POST)
        if  form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            is_default = form.cleaned_data["default"]
            if is_default:
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)
                default_address.shipping = new_address
                default_address.save()

            if next_page is not None:
                return HttpResponseRedirect(reverse(str(next_page))+"?address_added=True")
        else:
            raise Http404

