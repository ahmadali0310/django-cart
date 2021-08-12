from django.shortcuts import render
from .models import Product, Order, OrderItem
from django.http import JsonResponse
import json
from decimal import Decimal

# Create your views here.

import json

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def main(request):
    products = Product.objects.all()

    return render(request, 'store.html', {'products': products})



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {}
    return render(request, 'cart.html', {'items': items, 'order':order})



def update_cart(request):
    productId = request.POST.get('productId')
    action = request.POST.get('action')
    product = Product.objects.get(pk=productId)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer , complete=False)

    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity +=1
    
    if action == 'remove':
        orderitem.quantity -=1
    
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse(json.dumps({'quantity': orderitem.quantity, 'id': product.id, "get_product_total": orderitem.get_product_total, "get_items_quantity": order.get_items_quantity, "get_items_total": order.get_items_total}, cls=JSONEncoder), safe=False)


