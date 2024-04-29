from django.http import HttpRequest
from django.shortcuts import render
from account.models import User
from service.models import Service, Specialty
# Create your views here.


def order_form(request: HttpRequest, lawyer_id):
   try:
      lawyer = User.objects.get(pk=lawyer_id)
      service = Service.objects.create(lawyer=lawyer,
                                       customar=request.user,
                                       order_type=Specialty.objects.get(
                                          pk=request.POST['service']),
                                       subject=request.POST['subject'],
                                       content=request.POST['message'],
                                       file=request.FILES.get('file'))
   except User.DoesNotExist:
      return render(request, "404.html")

   return render(request, 'service/Service-request-form.html', {"lawyer": lawyer})


def payment_view(request):
   return render(request, 'service/payment.html')


def chat_view(request):
   return render(request, 'service/chat.html')


def current_orders(request):
   return render(request, 'service/Lawyers_orders.html')


def previous_orders(request):
   return render(request, 'service/previous_orders.html')


def order_details(request):
   return render(request, 'service/order_details.html')


def add_offer(request):
   return render(request, 'service/add_offer.html')


def rating_view(request):
   return render(request, 'service/rating.html')
