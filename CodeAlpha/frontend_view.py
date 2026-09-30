from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from itertools import product

from django.shortcuts import render, redirect
from AppApi.models import Register, Product, Cart
from django.contrib.auth.hashers import make_password, check_password




def register(request):

    if request.method == "POST":
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        if Register.objects.filter(email=request.POST["email"]).exists():
            return render(request, "register.html", {"error": "Email already registered"})

        Register.objects.create(
            full_name=request.POST["full_name"],
            email=request.POST["email"],
            mobile=request.POST["mobile"],
            password=make_password(password)
        )
        return redirect("login")

    return render(request, "register.html")



def login(request):

    if request.session.get("user_id"):
        user = Register.objects.filter(id=request.session["user_id"]).first()
        if user:
            return redirect("home")
        else:
            request.session.flush()

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = Register.objects.filter(email=email).first()

        if user and check_password(password, user.password):
            request.session.flush()
            request.session["user_id"] = user.id
            request.session["user_email"] = user.email
            request.session.save()
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
    
    products = Product.objects.filter(gender='accessories')
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
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return redirect("home")
    user_id = request.session.get("user_id")
    if user_id:
        user = Register.objects.filter(id=user_id).first()
        if user:
            cart_item, created = Cart.objects.get_or_create(user=user, product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
    else:
        session_cart = request.session.get("cart", {})
        pid = str(product_id)
        session_cart[pid] = session_cart.get(pid, 0) + 1
        request.session["cart"] = session_cart
        request.session.modified = True
    return redirect("cart")


def update_cart(request, cart_id):
    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.session.get("user_id")
        if user_id:
            cart_item = Cart.objects.filter(id=cart_id).first()
            if cart_item:
                if action == "increase":
                    cart_item.quantity += 1
                    cart_item.save()
                elif action == "decrease":
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                    else:
                        cart_item.delete()
        else:
            session_cart = request.session.get("cart", {})
            pid = str(cart_id)
            if pid in session_cart:
                if action == "increase":
                    session_cart[pid] += 1
                elif action == "decrease":
                    session_cart[pid] -= 1
                    if session_cart[pid] <= 0:
                        del session_cart[pid]
                request.session["cart"] = session_cart
                request.session.modified = True
    return redirect("cart")


def remove_from_cart(request, cart_id):
    user_id = request.session.get("user_id")
    if user_id:
        Cart.objects.filter(id=cart_id).delete()
    else:
        session_cart = request.session.get("cart", {})
        pid = str(cart_id)
        if pid in session_cart:
            del session_cart[pid]
        request.session["cart"] = session_cart
        request.session.modified = True
    return redirect("cart")


def cart(request):
    user_id = request.session.get("user_id")
    cart_items = []
    grand_total = 0
    if user_id:
        user = Register.objects.filter(id=user_id).first()
        if user:
            db_items = Cart.objects.filter(user_id=user_id).select_related("product")
            for item in db_items:
                item.product.discount_price = item.product.price - (item.product.price * item.product.discount / 100)
                item.total = item.product.discount_price * item.quantity
                cart_items.append(item)
    else:
        session_cart = request.session.get("cart", {})
        for pid, qty in session_cart.items():
            product = Product.objects.filter(id=pid).first()
            if product:
                product.discount_price = product.price - (product.price * product.discount / 100)
                cart_items.append({
                    "id": pid,
                    "product": product,
                    "quantity": qty,
                    "total": product.discount_price * qty,
                })
    grand_total = sum(item["total"] if isinstance(item, dict) else item.total for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "grand_total": grand_total})


def order(request):
    return render(request, "order.html")
def profile(request):
       return render(request,"profile.html")
def logout(request):
    request.session.flush()
    return redirect("login")
def Account_Business(request):
       return render(request,"Account_Business.html")


