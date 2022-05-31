from marketing.models import MarketingMessage, Slider
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product 
from .models import ProductImage


def index(request):
    sliders = Slider.objects.all()
    products = Product.objects.all()
    marketing_message = MarketingMessage.objects.all()[0]
    context = {"products": products, "marketing_message": marketing_message, "sliders": sliders}
    return render(request, 'index.html', context)


def search(request):
    try:
        q = request.GET.get('q')
    except:
        q = None
    if q:
        products = Product.objects.filter(title__icontains=q)
        context = {'query': q, 'products': products}
        template = 'results.html'
    else:
        template= 'home.html'
    return render(request, template, context) 



def product(request):
    contex = Product.objects.all()
    return render(request, "all.html", {'products': contex })

    

def singel_product(request, slug):
    product = Product.objects.get(slug= slug)
    images = ProductImage.objects.filter(product=product)
    #images = product.productimage.set.all()    
    context = {'product': product, 'images': images}
    return render(request, "singel.html", context)


