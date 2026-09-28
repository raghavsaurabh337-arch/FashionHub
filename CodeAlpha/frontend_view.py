from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from itertools import product

from django.shortcuts import render, redirect
from AppApi.models import Register, Product, Cart
from django.contrib.auth.hashers import make_password, check_password




def register(request):

    if request.method == "POST":

        password = request.POST["password"]

        Register.objects.create(
            full_name=request.POST["full_name"],
            email=request.POST["email"],
            mobile=request.POST["mobile"],
            password=make_password(password)
        )

        return redirect("login")

    return render(request, "register.html")



def login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Register.objects.filter(email=email).first()

        if user and check_password(password, user.password):

            request.session["user_id"] = user.id
            request.session["user_email"] = user.email

            return redirect("home")

        return render(request, "login.html", {"error": "Invalid email or password"})

    return render(request, "login.html")



# @login_required(login_url="login")
def home(request):

    products = Product.objects.all()
    for product in products:
                 product.name = product.name.capitalize()   
                 product.brand = product.brand.capitalize()
                 product.size = product.size.upper()    
                 product.description = product.description.title()
                 product.color = product.color.capitalize()
                 product.discount_price = product.price - (product.price * product.discount / 100)
    return render(request, "home.html", {"products": products})



def products(request):
    products = Product.objects.all()
    for product in products:
             product.name = product.name.capitalize()
             product.color = product.color.capitalize()
             product.brand = product.brand.capitalize()
             product.size = product.size.upper()
             product.description = product.description.title()
                         
             product.discount_price = product.price - (product.price * product.discount / 100)
    return render(request, "products.html", {"products": products})

def women(request):
    products = Product.objects.filter(gender='female')
    for product in products:
                 product.name = product.name.capitalize()
                 product.color = product.color.capitalize()
                 product.brand = product.brand.capitalize()
                 product.size = product.size.upper()
                 product.description = product.description.title()
                 product.discount_price = product.price - (product.price * product.discount / 100)

    return render(request, "women.html", {"products": products})


def men(request):
    products = Product.objects.filter(gender='male')
    for product in products:
                 product.name = product.name.capitalize()
                 product.color = product.color.capitalize()
                 product.brand = product.brand.capitalize()
                 product.size = product.size.upper()
                 product.description = product.description.title()
                 product.discount_price = product.price - (product.price * product.discount / 100)
    return render(request, "men.html", {"products": products})


def kids(request):
    products = Product.objects.filter(gender='kids')
    for product in products:
                 product.name = product.name.capitalize()
                 product.color = product.color.capitalize()
                 product.brand = product.brand.capitalize()
                 product.size = product.size.upper()
                 product.description = product.description.title()
                 product.discount_price = product.price - (product.price * product.discount / 100)
    return render(request, "kids.html", {"products": products})


def Accessories(request):
    
    products = Product.objects.filter(name__icontains='watch')
    for product in products:
                 product.name = product.name.capitalize()
                 product.color = product.color.capitalize()
                 product.brand = product.brand.capitalize()
                 product.size = product.size.upper()
                 product.description = product.description.title()
                 product.discount_price =  product.price - (product.price *    product.discount / 100)
    return render(request, "Accessories.html", {"products": products})

def products_details(request):
    
    return render(request, "products_details.html")


def add_to_cart(request, product_id):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = Register.objects.get(id=user_id)
    product = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("cart")


def update_cart(request, cart_id):
    if request.method == "POST":
        cart_item = Cart.objects.filter(id=cart_id).first()
        if cart_item:
            action = request.POST.get("action")
            if action == "increase":
                cart_item.quantity += 1
                cart_item.save()
            elif action == "decrease":
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
    return redirect("cart")


def remove_from_cart(request, cart_id):
    Cart.objects.filter(id=cart_id).delete()
    return redirect("cart")


def cart(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    cart_items = Cart.objects.filter(user_id=user_id).select_related("product")
    for item in cart_items:
        item.product.discount_price = item.product.price - (item.product.price * item.product.discount / 100)
        item.total = item.product.discount_price * item.quantity
    grand_total = sum(item.total for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "grand_total": grand_total})


def order(request):
    return render(request, "order.html")
def profile(request):
       return render(request,"profile.html")
def logout(request):
       return render(request,"logout.html")
def Account_Business(request):
       return render(request,"Account_Business.html")


