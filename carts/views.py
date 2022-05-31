from django.shortcuts import render, HttpResponseRedirect 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from products.models import Product 
from .models import Variation
from .models import CartItem
from .models import Cart



# Create your views here.


def view(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id= the_id)
    except:
        the_id = None
    if the_id:
        new_total = 0.00
        for item in cart.cartitem_set.all():
            line_total = float(item.product.price) * item.quantity
            new_total += line_total
        request.session['items_total'] = cart.cartitem_set.count()
        cart.total = new_total
        cart.save() 
        context = {'cart': cart}
    else:
        empty_message = "Yout cart is empty keep shopping"
        context = {'empty':True, 'empty_message': empty_message}
    return render(request, "view.html", context)

    
def remove_from_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return redirect('cart')
    
    cartitem = CartItem.objects.get(id=id)
    # cartitem.cart = None
    # cartitem.save()
    cartitem.delete()
    #send "sucsess message"
    return redirect('cart')
        




def add_to_cart(request, slug,):
    request.session.set_expiry(6000)
    
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)

    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass

    product_var = [] #product variation
    if request.method == 'POST':
        qty = request.POST['qty']  
        for item in request.POST:
            key = item
            val = request.POST[key]
            try:
                v = Variation.objects.get(product=product, category__iexact= key, title__iexact= val)
                product_var.append(v)
            except:
                pass
        ("cart item object", "true/")
        cart_item = CartItem.objects.create(cart=cart, product=product)
        if len(product_var) > 0:
            cart_item.variations.add(*product_var)
        cart_item.quantity = qty
        cart_item.save()

        #sucsess message
        return redirect('cart')
    #error
    return redirect('cart')
    