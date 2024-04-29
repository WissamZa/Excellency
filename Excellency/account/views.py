from django.shortcuts import render, redirect
from django.http import HttpRequest
from account.models import User, LawyerProfile, CustomarProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.models import Post
from account.models import Specialty, Specialty_CHOICES
from main.validator import validat
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError


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
               specialties = [Specialty_CHOICES.get(
                   s) for s in request.POST.getlist("specialty")]
               user_profile = LawyerProfile.objects.create(
                  user=new_user,

                  image=request.FILES["image"],
                  gender=request.POST["gender"],
                  phone=validat(phone=request.POST.get("phone")),
                  licence=request.FILES["licence"],
                  Qualification=request.FILES["Qualification"])
               specialty_id = Specialty.objects.filter(
                  name__in=specialties)
               for spec in specialty_id:
                  user_profile.specialty.add(spec)

            if request.POST["role"] == "Customar":
               CustomarProfile.objects.create(
                  user=new_user,
                  phone=validat(phone=request.POST.get("phone")),
               )
            subject = 'نشكرك على تسجيلك في موقع معالي '
            message = f'''مرحبا  {new_user.full_name},\n\
                نحن سعداء بتواجدك هنا. نتطلع إلى تقديم خدماتنا لك بأفضل شكل ممكن وتلبية احتياجاتك وتطلعاتك. سواء كنت تبحث عن استشارة قانونية، أو ترغب في الوصول إلى معلومات قانونية مفيدة، فإننا هنا لمساعدتك.

لا تتردد في استكشاف الموارد المتاحة لدينا، ولا تتردد في الاتصال بنا إذا كان لديك أي استفسار أو اقتراح. نحن هنا لخدمتك وتقديم الدعم الذي تحتاجه.

شكرًا لثقتك بنا، ونتمنى لك تجربة ممتعة ومفيدة على منصتنا.

تحياتنا،
فريق المعالي للمحاماة .'''
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

   except Exception as e:
      msg = "Something went wrong. Please try again."

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


@login_required(login_url="/account/login")
def update_profile_view(request: HttpRequest, user_id):
   specialties = Specialty.objects.all()
   user: User = request.user

   if request.method == "POST":
      with transaction.atomic():
         user.full_name = validat(full_name=request.POST.get("full_name"))
         user.save()
         if request.POST["role"] == "Lawyer":
            lawyer_profile = LawyerProfile.objects.get(user=user)
            lawyer_profile.image = request.FILES.get(
                "image", lawyer_profile.image)
            lawyer_profile.about = request.POST.get(
               "about", lawyer_profile.about)
            post_specialties = request.POST.getlist("specialty")

            lawyer_profile.gender = request.POST.get(
                "gender", lawyer_profile.gender)
            lawyer_profile.phone = validat(
                phone=request.POST.get("phone", lawyer_profile.phone))
            lawyer_profile.licence = request.FILES.get(
                "licence", lawyer_profile.licence)
            lawyer_profile.bannar = request.FILES.get(
                "back-image", lawyer_profile.bannar)
            lawyer_profile.Qualification = request.FILES.get(
             "Qualification", lawyer_profile.Qualification)

            lawyer_profile.specialty.clear()
            specialty_id = Specialty.objects.filter(
                name__in=post_specialties)
            for spec in specialty_id:
               lawyer_profile.specialty.add(spec)
            lawyer_profile.save()

         if request.POST["role"] == "Customar":
            user.full_name = validat(full_name=request.POST.get("full_name"))
            user.save()
            customar_profile: CustomarProfile = CustomarProfile.objects.get(
               user=user)
            print(request.FILES.get("image"))
            customar_profile.image = request.FILES.get(
                "image", customar_profile.image)
            customar_profile.bannar = request.FILES.get(
                "back-image", customar_profile.bannar)
            customar_profile.phone = validat(phone=request.POST.get(
               "phone", customar_profile.phone))
            customar_profile.save()
         return redirect("account:profile_view", user_id=user.pk)
   return render(request, "account/update_profile.html", {"specialties": specialties})


def account_balance(request):
   return render(request, 'account/account_balance.html')


def profile_view(request: HttpRequest, user_id):
   try:
      user = User.objects.get(pk=user_id)
      user_profile = None
      if user.role == "Lawyer":
         user_profile = user.lawyer_profile
      if user.role == "Customar":
         user_profile = user.customar_profile
         print(user_profile.image.url)
      if request.method == "POST":
         Post.objects.create(author=request.user,
                             title=request.POST.get('title'),
                             content=request.POST.get('content'),
                             image=request.FILES.get('image'))
   except User.DoesNotExist:
      return render(request, "404.html")

   return render(request, "account/profile.html", {"user": user,
                                                   "user_profile": user_profile})
