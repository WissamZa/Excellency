from django.shortcuts import render, redirect
from django.http import HttpRequest
from account.models import User, LawyerProfile, CustomarProfile
from django.contrib.auth import authenticate, login, logout
from account.models import Specialty, Specialty_CHOICES
from main.validator import validat, validate_national_id
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.urls import reverse


from django.conf import global_settings as settings
from django.core.mail import send_mail


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
            email = validat(email=request.POST.get("email"))
            new_user = User.objects.create(
               full_name=validat(full_name=request.POST.get("full_name")),
               role=request.POST["role"],
                national_id=validat(
                   national_id=request.POST.get("national_id")),
                username=email,
                email=email)
            new_user.set_password(request.POST.get("password"))
            new_user.save()
            if request.POST["role"] == "Lawyer":

               user_profile = LawyerProfile.objects.create(
                  user=new_user,

                  image=request.FILES["image"],
                  gender=request.POST["gender"],
                  phone=validat(phone=request.POST.get("phone")),
                  licence=request.FILES["licence"],
                  Qualification=request.FILES["Qualification"])
               specialty_id = Specialty.objects.get(
                  name=Specialty_CHOICES.get(request.POST["specialty"])).pk
               user_profile.specialty.add(specialty_id)

            if request.POST["role"] == "Customar":
               CustomarProfile.objects.create(
                  user=new_user,
                  image=request.POST.get(
                     "image", CustomarProfile.image.field.default),
                  phone=validat(phone=request.POST.get("phone")),
               )
            subject = 'نشكرك على تسجيلك في موقع معالي '
            message = f"مرحبا  {new_user.full_name},\n\
              نشكرك على تسجيلك ."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [new_user.email, ]
            send_mail(subject, message, email_from, recipient_list)
         return redirect("account:login_view")

   except IntegrityError as e:
      msg = "الهوية الوطنية أو البريد الالكتروني مستخدم بالفعل. حاول مرة اخرى..."
      print(e)
   except ValidationError as e:
      msg = e.message
      return render(request, "account/sign_up.html",
                    {"msg": msg,
                     "Specialty": [(k, v) for k, v in Specialty_CHOICES.items()],
                     "post": request.POST})

   # except Exception as e:
   #    msg = "Something went wrong. Please try again."
   #    print(e.with_traceback())
   return render(request, "account/sign_up.html", {"msg": msg, "Specialty": [(k, v) for k, v in Specialty_CHOICES.items()]})


def login_view(request: HttpRequest):
   msg = None
   next = None
   try:
      if request.user.is_authenticated:
         return redirect("main:index_view")
      if "next" in request.GET:
         next = request.GET.get("next", "")

      if request.method == "POST":
         # authenticat user
         user = None
         # if validate_national_id(request.POST["username"]):
         #    user = authenticate(
         #     request,
         #     national_id=request.POST["username"],
         #     password=request.POST.get("password")
         #        )
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
   except ValidationError:
      msg = "الهوية الوطنية أو الايميل مستخدم خاطئ. حاول مرة اخرى..."

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


# def user_profile_view(request: HttpRequest):

#    return render(request, "account/user_profile.html")


# def update_profile_view(request: HttpRequest, user_name):
#    if not (request.user.is_authenticated and request.user.username == user_name):
#       return render(request, "main/no_permission.html")
#    user: User = request.user

#    if request.method == "POST":
#       user.full_name = request.POST.get(
#           'full_name', user.full_name)
#       # Lawyer Profile update
#       if user.role == "Lawyer":
#          lawyer_profile: LawyerProfile = user.LawyerProfile
#          lawyer_profile.phone = validat(
#             phone=request.POST.get('phone', lawyer_profile.phone))
#          lawyer_profile.gender = request.POST.get(
#             'gender', lawyer_profile.gender)
#          lawyer_profile.image = request.FILES.get(
#             'image', lawyer_profile.image)
#          lawyer_profile.about = request.POST.get(
#             'about', lawyer_profile.about)
#          lawyer_profile.licence = request.FILES.get("licence",),
#          lawyer_profile.Qualification = request.FILES.get(
#              "qualification", lawyer_profile.Qualification)
#          specialties = Specialty.objects.filter(
#            name=Specialty_CHOICES.get(request.POST["specialty"], lawyer_profile.specialty.all()))
#          lawyer_profile.specialty.add(id.pk for id in specialties)
#          lawyer_profile.save()

#          # customar profile Update
#          if user.role == "Customar":
#             customar_profile: CustomarProfile = user.CustomarProfile
#          customar_profile.gender = request.POST.get(
#             'gender', customar_profile.gender)
#          customar_profile.image = request.FILES.get(
#             'image', customar_profile.image)
#          customar_profile.save()
#          user.save()
#          return redirect("account:profile_view", user_name=user.username)

#    return render(request, "account/update_profile.html", {"user": user, "specialty_choices": Specialty_CHOICES})


def update_profile_view(request: HttpRequest, user_id):
   specialties = Specialty.objects.all()
   return render(request, "account/update_profile.html", {"specialties": specialties})


def account_balance(request):
   return render(request, 'account/account_balance.html')


def profile_view(request: HttpRequest, user_id):

   user = User.objects.get(pk=user_id)
   return render(request, "account/profile.html", {"user": user})
