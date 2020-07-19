from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .decorators import unauthenticated_user
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm, CustomerForm
from .utils import cart_data, save_cookie_item_logged_user


# Create your views here.
# login user
@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            save_cookie_item_logged_user(request)
            response = redirect('home_page')
            # response = HttpResponse("Cookies Cleared")
            response.delete_cookie("cart")
            return response
        else:
            messages.warning(request, 'Invalid username or password')

    context = {}
    return render(request, 'store/login.html', context)


# signup users
@unauthenticated_user
def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + username)
            return redirect('login_page')

    context = {'form': form}
    return render(request, 'store/register.html', context)


# profile page
@login_required(login_url='login_page')
def profile(request):
    customer_details = request.user
    form = CustomerForm(instance=customer_details)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer_details)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile information successfully updated...')
    data = cart_data(request)
    cart_items = data['cart_items']
    shipping_address = ShippingAddress.objects.filter(customer=request.user.customer)
    orders = Order.objects.filter(customer=request.user.customer, complete=True)
    context = {'form': form, 'cart_items': cart_items,
               'shipping_address': shipping_address, 'orders': orders}
    return render(request, 'store/profile.html', context)


# logout user
def logout_page(request):
    logout(request)
    return redirect('home_page')


# home page
def home_page(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    # order = data['order']
    # items = data['items']

    context = {'cart_items': cart_items}
    return render(request, 'store/home.html', context)


# product list page
def store_page(request):
    if request.method == 'GET' and 'k' in request.GET:
        request_key = request.GET['k']
        if request_key == '':
            return redirect('store_page')
    else:
        request_key = ''

    data = cart_data(request)
    cart_items = data['cart_items']
    # order = data['order']
    # items = data['items']

    products = Product.objects.filter(name__contains=request_key)
    context = {'products': products, 'cart_items': cart_items}
    return render(request, 'store/store.html', context)


# product details page
def product_details(request, slug):
    data = cart_data(request)
    cart_items = data['cart_items']
    try:
        product = Product.objects.get(slug=slug)
    except:
        product = False

    context = {'product': product, 'cart_items': cart_items}

    if product:
        return render(request, 'store/product_details.html', context)
    else:
        return render(request, 'store/page_not_found.html', context)


# cart page
def cart_page(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}

    # check cart item if cart is empty loads empty cart page and shop again
    if cart_items == 0:
        return render(request, 'store/cart_empty.html', context)

    return render(request, 'store/cart.html', context)


# shows the check out page
@login_required(login_url='login_page')
def checkout_page(request):
    data = cart_data(request)
    cart_items = data['cart_items']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}

    # check cart item if cart is empty loads empty cart page and shop again
    if cart_items == 0:
        # messages.warning(request, 'Empty cart , add product to your cart')
        # return redirect('store_page')
        return render(request, 'store/cart_empty.html', context)

    return render(request, 'store/checkout.html', context)


# add or remove cart items
def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.customer

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    product = Product.objects.get(id=product_id)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)
    elif action == 'remove_item':
        order_item.quantity = 0

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    cart_updated = JsonResponse('cart updated', safe=False)
    return cart_updated


# place order
def process_order(request):
    if request.user.is_authenticated:

        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == float(order.get_cart_total):
            order.complete = True

        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zip=data['shipping']['zipcode'],
            )

        # print('Data', data)
        return JsonResponse('order placed', safe=False)

    else:

        return JsonResponse('Login required', safe=False)
