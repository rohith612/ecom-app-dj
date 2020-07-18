import json
from .models import *


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        # get the order or created it if empty
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # get the items associated with it
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        cart_items = cookie_data['cart_items']
        order = cookie_data['order']
        items = cookie_data['items']

    return {'items': items, 'order': order, 'cart_items': cart_items}


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0, 'shipping': False}
    cart_items = order['get_cart_items']

    for i in cart:

        try:
            cart_items += cart[i]['quantity']
            # get product from the cart cookies

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    return {'items': items, 'order': order, 'cart_items': cart_items}


def save_cookie_item_logged_user(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    for i in cart:
        try:
            product = Product.objects.get(id=i)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart[i]['quantity']
            )
            # order_item.quantity = cart[i]['quantity']
            # order_item.save()
        except:
            pass

    return 1
