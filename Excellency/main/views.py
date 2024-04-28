from os import name
from django.http import HttpRequest
from django.shortcuts import render
from main.models import Contactus
from account.models import User, Specialty,LawyerProfile
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
      lawyers = User.objects.filter(role="Lawyer")
      spcialities = Specialty.objects.all()

      if "lawyer_name" in request.GET:
         lawyers = lawyers.filter(
            full_name__contains=request.GET.get("lawyer_name")
         )
      if "spcialties" in request.GET:
         spcialities_filter = request.GET.getlist("spcialties")
         lawyers = lawyers.filter(
            lawyer_profile__specialty__in=spcialities_filter).annotate(Count("id"))
   except Exception as e:
      print(e)
   return render(request, "main/lawyers.html", {"lawyers": lawyers, "specialities": spcialities})


def contact_messages(request):

    return render(request, 'main/contact_messages.html')

def admin_viwe(request):
    lawyer_profiles = LawyerProfile.objects.all()
    return render(request, 'main/admin.html', {'lawyer_profiles': lawyer_profiles})

def lawyer_details_view(request):
    return render(request, 'main/lawyer_details.html')
 
def post_view(request):
    return render(request, 'main/post_lawyers.html')

