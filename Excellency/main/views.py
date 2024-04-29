from os import name
from django.http import HttpRequest
from django.shortcuts import render, redirect
from main.models import Contactus, Post
from account.models import User, Specialty, LawyerProfile
from django.db.models import Count


def index_view(request: HttpRequest):
   return render(request, "main/index.html")


def contactus_view(request: HttpRequest):
   msg = None
   try:
      if request.method == "POST":
         Contactus.objects.create(full_name=request.POST.get('full_name'),
                                  email=request.POST.get('email'),
                                  subject=request.POST.get('subject'),
                                  message=request.POST.get('message'),
                                  )
         msg = "تم ارسال رسالتك بنجاح"
   except Exception as e:
      pass
   return render(request, "main/contactus.html", {'msg': msg})


def check_lawyer_has_specialty(lawyer: User, specialty):
   if specialty in lawyer.lawyer_profile.specialty.all():
      return True
   return False


def lawyers_view(request: HttpRequest):
   try:
      lawyers = User.objects.filter(
         role="Lawyer", lawyer_profile__certified=True).order_by("full_name")
      spcialities = Specialty.objects.all()

      if "lawyer_name" in request.GET:
         lawyers = lawyers.filter(
            full_name__contains=request.GET.get("lawyer_name")
         )
      if "spcialties" in request.GET:
         spcialities_filter = request.GET.getlist("spcialties")
         lawyers = lawyers.filter(
            lawyer_profile__specialty__in=spcialities_filter).annotate(Count("id"))
      if "sort" in request.GET:
         if request.GET.get("sort") == "user_name_a_z":
            lawyers = lawyers.order_by("full_name")
         if request.GET.get("sort") == "user_name_z-a":
            lawyers = lawyers.order_by("-full_name")
         if request.GET.get("sort") == "rating_top":
            pass
   except Exception as e:
      print(e)
   return render(request, "main/lawyers.html", {"lawyers": lawyers, "specialities": spcialities})


def contact_messages(request: HttpRequest):

   messages = Contactus.objects.all()

   return render(request, 'main/contact_messages.html', {'messages': messages})


def admin_viwe(request):
   lawyer_profiles = LawyerProfile.objects.all()
   return render(request, 'main/admin.html', {'lawyer_profiles': lawyer_profiles})


def lawyer_details_view(request):
   return render(request, 'main/lawyer_details.html')


def post_list(request):
   if request.user.is_authenticated:
      posts = Post.objects.all()
      return render(request, 'main/post_lawyers.html', {'posts': posts})
   else:
      return redirect('account:login_view')
