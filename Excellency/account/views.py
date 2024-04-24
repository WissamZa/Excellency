from click import File
from django.shortcuts import render, redirect
from django.http import HttpRequest
from account.models import User, LawyerProfile, CustomarProfile
from django.contrib.auth import authenticate, login, logout
from service.models import Specialty_CHOICES
from main.validator import validat
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.urls import reverse


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
            new_user = User.objects.create(
               full_name=request.POST.get("full_name"),
                national_id=validat(
                   national_id=request.POST.get("national_id")),
                email=validat(email=request.POST.get("email")),
                password=validat(password=request.POST.get("password"))
            )
            if request.POST["role"] == "Lawyer":

               user_profile = LawyerProfile.objects.create(
                  user=new_user,
                  image=request.FILES["image"],
                  gender=request.POST["gender"],
                  phone=validat(phone=request.POST.get("phone")),
                  licence=request.FILES.get("licence"),
                  Qualification=request.FILES.get("qualification"))
               S
               user_profile.specialty.add(name=request.POST["specialty"])

            if request.POST["role"] == "Customar":
               CustomarProfile.objects.create(
                  user=new_user,
                  image=request.POST.get(
                     "image", CustomarProfile.image.field.default),
                  gender=request.POST["gender"],
                  phone=validat(phone=request.POST.get("phone")),
               )

         return redirect("account:login_view")

   except IntegrityError as e:
      msg = "اسم المستخدم أو الايميل مستخدم بالفعل. حاول مرة اخرى..."
      print(e)
   except ValidationError as e:
      msg = e.message
   # except Exception as e:
   #    msg = "Something went wrong. Please try again."
   #    print(e.with_traceback())

   return render(request, "account/sign_up.html", {"msg": msg, "Specialty": Specialty_CHOICES})


def login_view(request: HttpRequest):
   msg = None
   next = None
   if request.user.is_authenticated:
      return redirect("main:index_view")
   if "next" in request.GET:
      next = request.GET.get("next", "")

   if request.method == "POST":
      # authenticat user
      user_name = None
      if validat(national_id=request.POST["username"]):
         user = authenticate(
          request,
          national_id=request.POST["username"],
          password=request.POST.get("password")
             )
      if validat(email=request.POST["username"]):
         user = authenticate(
          request,
          email=request.POST["username"],
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

   return render(request, "account/update_profile.html", {"user": user})
