from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from product.models import Product
from .models import Cart, Profile
from main.validator import validat
from django.core.exceptions import ValidationError

from django.db import transaction, IntegrityError


def sign_up_view(request: HttpRequest):
   try:
      msg = None
      if request.user.is_authenticated:
         return redirect("main:index_view")
      if request.method == "POST":
         with transaction.atomic():
            # create new user
            if request.POST.get("password") != request.POST.get("confirm_password"):
               msg = "Invalid password"
               raise IntegrityError(msg)
            new_user = User.objects.create_user(
                username=validat(username=request.POST.get("username")),
                email=validat(email=request.POST.get("email")),
                password=validat(password=request.POST.get("password"))
            )

            Profile.objects.create(
               user=new_user,
               phone=validat(phone=request.POST.get("phone")))

         return redirect("account:login_view")

   except IntegrityError as e:
      msg = "اسم المستخدم أو الايميل مستخدم بالفعل. حاول مرة اخرى..."
      print(e)
   except ValidationError as e:
      msg = e.message
   # except Exception as e:
   #    msg = "Something went wrong. Please try again."
   #    print(e.with_traceback())

   return render(request, "account/sign_up.html", {"msg": msg})


def login_view(request: HttpRequest):
   msg = None
   next = None
   if request.user.is_authenticated:
      return redirect("main:index_view")
   if "next" in request.GET:
      next = request.GET.get("next", "")

   if request.method == "POST":
      # authenticat user
      user = authenticate(
          request,
          username=request.POST.get("username"),
          password=request.POST.get("password")
      )
      if user:
         # login user
         login(request, user)

         return redirect(request.POST.get("next") or "main:index_view")
      else:
         msg = "اسم المستخدم أو الايميل مستخدم خاطئ. حاول مرة اخرى..."

   return render(request, "account/login.html", {"msg": msg,
                                                 "next": next})


def logout_view(request: HttpRequest):
   if request.user.is_authenticated:
      logout(request)
   return redirect('main:index_view')


def user_profile_view(request: HttpRequest, user_name):
   try:
      msg = None
      user = User.objects.get(username=user_name)
   except User.DoesNotExist:
      msg = "User Not Found"
      return render(request, "account/user_profile.html", {"msg": msg})
   return render(request, "account/user_profile.html", {"user": user})


def update_profile_view(request: HttpRequest, user_name):
   if not request.user.username == user_name:
      return render(request, "main/no_permission.html")
   user = request.user

   if request.method == "POST":
      user.first_name = request.POST.get('first_name', user.first_name)
      user.last_name = request.POST.get('last_name', user.last_name)
      user.profile.phone = validat(
         phone=request.POST.get('phone')) or user.profile.phone
      user.profile.gender = request.POST.get('gender', user.profile.gender)
      user.profile.about = request.POST.get('about', user.profile.gender)
      user.profile.address = request.POST.get('about', user.profile.gender)
      user.profile.nationality = request.POST.get(
         'nationality', user.profile.nationality)
      user.profile.avatar = request.FILES.get('avatar', user.profile.avatar)
      user.profile.save()
      user.save()
      return redirect("account:user_profile_view", user_name=user.username)

   return render(request, "account/update_profile.html", {"user": user,
                                                          "nationality": Profile.nationality_choices.choices,
                                                          "genders": Profile.gender_choices.choices, })


def cart_view(request: HttpRequest, username):
   try:
      if not request.user.username == username:
         return render(request, "main/no_permission.html")
      total: float = 0.0
      user = request.user
      cart = Cart.objects.filter(user=user).order_by('-added_date')
      for item in cart:
         total = total + (item.product.price * item.quantity)
      if request.method == 'POST':
         product = Product.objects.get(id=request.POST.get('product_id'))
         item = cart.get(product=product)
         item.quantity = request.POST.get('quantity')
         item.save()

   except Exception as e:
      print(e)
   return render(request, "account/cart.html", {"cart": cart, "total": total})


def delete_product_view(request: HttpRequest, username, cart_id):

   try:
      cart = Cart.objects.get(id=cart_id)
      if request.user.is_authenticated and cart.user.username == request.user.username:
         cart.delete()
         return redirect("account:cart_view", username=request.user.username)
      else:
         return render(request, "main/no_permission.html")

   except Exception as e:
      print(e)
