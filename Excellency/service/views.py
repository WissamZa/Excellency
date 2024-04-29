from django.http import HttpRequest
from django.shortcuts import redirect, render
from account.models import LawyerProfile, User
from django.contrib.auth.decorators import login_required
from service.models import Service, Specialty
from django.db.models import Q
# Create your views here.


@login_required(login_url='/account/login')
def order_form(request: HttpRequest, lawyer_id):
   try:
      lawyer = User.objects.get(pk=lawyer_id)
      if request.user == lawyer:
         return render(request, "404.html")
      if request.method == 'POST':
         order = Service.objects.create(lawyer=lawyer,
                                        customar=request.user,
                                        order_type=Specialty.objects.get(
                                            pk=request.POST['service']),
                                        subject=request.POST['subject'],
                                        content=request.POST['message'],
                                        file=request.FILES.get('file'))
         return redirect("service:order_details", order_id=order.id)
   except User.DoesNotExist:
      return render(request, "404.html")

   return render(request, 'service/Service-request-form.html', {"lawyer": lawyer})


@login_required(login_url="/account/login")
def payment_view(request):
   return render(request, 'service/payment.html')


@login_required(login_url="/account/login")
def chat_view(request):
   return render(request, 'service/chat.html')


@login_required(login_url="/account/login")
def current_orders(request):
   user = request.user
   orders = Service.objects.filter(Q(lawyer=user) | Q(customar=user))
   return render(request, 'service/Lawyers_orders.html', {"orders": orders})


@login_required(login_url="/account/login")
def previous_orders(request):
   return render(request, 'service/previous_orders.html')


@login_required(login_url="/account/login")
def order_details(request: HttpRequest, order_id):
   user = request.user
   order = Service.objects.get(id=order_id)

   if not (order.lawyer == user or order.customar == user):
      return render(request, "no_permission.html")

   if request.method == "POST":
      if "reject-btn" in request.POST:
         order.status = request.POST.get("status", order.status)
         order.save()
      if "make_offer" in request.POST:
         order.price = request.POST.get("price")
         order.status = request.POST.get("status", order.status)
         order.save()

   return render(request, 'service/order_details.html', {"order": order,
                                                         "status_choices": dict(Service.STATUS_CHOICES)})


def add_offer(request):
   return render(request, 'service/add_offer.html')


def rating_view(request):
   return render(request, 'service/rating.html')
