import stripe
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Category, Product, Comment, ShippingAddress
from .forms import RegisterForm, LoginForm, CommentForm, BookForm
from .utils import CartAuthenticatedUser


def index(request):
    data = {
        'products': Product.objects.all().order_by('-id')
    }
    return render(request, 'app/index.html', data)


def menu(request):
    data = {
        'products': Product.objects.all()
    }
    return render(request, 'app/menu.html', data)


def about(request):
    return render(request, 'app/about.html')


def detail(request, id):
    data = {
        'product': Product.objects.get(id=id),
        'form': CommentForm(),
        'comments': Comment.objects.filter(product_id=id)
    }
    return render(request, 'app/detail.html', data)


def save_comment(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            product = Product.objects.get(id=id)
            user = request.user
            form = CommentForm(data=request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = product
                comment.autor = user
                comment.save()
                messages.success(request, f"Komment qo'shildi!")
                return redirect('detail', id=id)
        else:
            return HttpResponse("No comment found!")
    else:
        messages.error(request, f"Komment qoldirish uchun avval ro'yxatdan o'ting!")
        return redirect('login')


def checkout(request):
    if request.method == 'POST':
        customer = request.user
        form = BookForm(data=request.POST)
        if form.is_valid():
            form.customer = customer
            form.save()
            messages.success(request, f"Buyurtmangiz tez orada yetib boradi!")
            return redirect('index')
    form = BookForm()
    data = {
        'form': form
    }
    return render(request, 'app/book.html', data)


def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']
    total_quantity = cart_info['cart_total_quantity']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Online shop mahsulotlaari'
                },
                'unit_amount': int(total_price * 100)
            },
            'quantity': total_quantity
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('success')),
    )
    return redirect(session.url, 303)


def success_payment(request):
    return render(request, 'app/success.html')


def cart(request):
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        data = {
            'order_products': cart_info['order_products'],
            'cart_total_price': cart_info['cart_total_price'],
            'cart_total_quantity': cart_info['cart_total_quantity']
        }
        return render(request, 'app/cart.html', data)
    else:
        messages.error(request, f"Avval ro'yxatdan o'ting!")
        return redirect('login')


def to_cart(request: HttpRequest, product_id, action):
    if request.user.is_authenticated:
        CartAuthenticatedUser(request, product_id, action)
        page = request.META.get('HTTP_REFERER')
        return redirect(page)
    else:
        messages.error(request, f"Xaridni amalga oshirish uchun ro'yxatdan o'ting!")
        return redirect('login')


def register_form(request):
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request,
                         f'{user.username} Registratsiya muvaffaqqiyatli yakunlandi!')
        return redirect('index')

    form = RegisterForm()
    data = {
        'form': form
    }
    return render(request, 'app/register.html', context=data)


def login_form(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'{user.username} Saytga xush kelibsiz!')
            return redirect('index')

        if form.errors:
            for error in form.errors.values():
                messages.error(request, f'{error}')

    form = LoginForm()
    data = {
        'form': form
    }
    return render(request, 'app/login.html', data)


def logout_user(request):
    logout(request)
    messages.warning(request, 'Siz saytdan chiqdingiz!')
    return redirect('login')


# ------------------------------------------------------------------------------------------
# Filter


def product_by_category(request, id):
    data = {
        'products': Product.objects.filter(category_id=id)
    }
    return render(request, 'app/index.html', data)


def order_by_alphabet(request):
    data = {
        'products': Product.objects.all().order_by('name')
    }
    return render(request, 'app/menu.html', data)


def order_by_alphabet_reverse(request):
    products = Product.objects.all().order_by('name')
    data = {
        'products': products.reverse()
    }
    return render(request, 'app/menu.html', data)


def order_by_price(request):
    data = {
        'products': Product.objects.all().order_by('price')
    }
    return render(request, 'app/menu.html', data)


def order_by_price_2(request):
    data = {
        'products': Product.objects.all().order_by('-price')
    }
    return render(request, 'app/menu.html', data)


def discount(request):
    data = {
        'products': Product.objects.filter(discount=True)
    }
    return render(request, 'app/menu.html', data)



