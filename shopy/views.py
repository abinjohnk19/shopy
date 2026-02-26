from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


# ================= HOME =================
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# ================= ADD TO CART =================
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart')


# ================= CART PAGE =================
@login_required
def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


# ================= REMOVE FROM CART =================
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('cart')


# ================= UPDATE QUANTITY =================
@login_required
def update_quantity(request, product_id):
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity'))

    if quantity > 0:
        cart[str(product_id)] = quantity
    else:
        cart.pop(str(product_id), None)

    request.session['cart'] = cart
    return redirect('cart')


# ================= CHECKOUT =================
@login_required
def order_product(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')

        last_order = None

        for item in cart_items:
            last_order = Order.objects.create(
                user=request.user,
                product=item['product'],
                customer_name=name,
                address=address,
                phone=phone,
                quantity=item['quantity'],
                total_price=item['subtotal'],
                payment_method=payment_method
            )

        # clear cart
        request.session['cart'] = {}

        return redirect('order_success', order_id=last_order.id)

    return render(request, 'order.html', {
        'cart_items': cart_items,
        'total': total
    })


# ================= ORDER SUCCESS =================
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})


# ================= MY ORDERS =================
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


# ================= PRODUCT DETAIL =================
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


# ================= REGISTER =================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# ================= LOGOUT =================
def custom_logout(request):
    logout(request)
    return redirect('home')