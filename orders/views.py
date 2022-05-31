import time
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect
import stripe
from accounts.forms import UserAddressForm
from accounts.models import UserAddress
from django.conf import settings
from carts.models import Cart
from .models import Order
from .utils import id_generator
from django.contrib.auth.decorators import login_required
# Create your views here.


# try:
stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
stripe_secret = settings.STRIPE_SECRET_KEY
stripe.api_key = stripe_secret
# except Exception:
#     print(str(e))
#     raise NotImplementedError(str(e))


def userorders(request):
    return render(request, "users.html")



@login_required
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse("/cart/"))
    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.save()
    except:
        # work on error message
         return HttpResponseRedirect(reverse("/cart/"))

    try:
        address_added = request.GET.get("address_added")
        
    except:
        address_added = None
    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None

    current_addresses = UserAddress.objects.filter(user=request.user)
    billing_addresses = UserAddress.objects.get_billing_addresses(user=request.user) 
    print(billing_addresses)
    #assign address
    #run credit card
    if request.method == "POST":
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retreive(user_stripe)
            print(customer)
            # print(request.POST['stripeToken']
        except:
            pass
            

    if new_order.status == "Finished":
        #cart.delete()
        del request.session['cart_id']
        del request.session['items_total']
        return HttpResponseRedirect(reverse("cart"))
    
    context = {
    "address_form": address_form,
    "current_addresses": current_addresses,
    "billing_addresses": billing_addresses,
    "strip_pub": stripe_pub,
     }
    template = "checkout.html"
    return render(request, template, context)

