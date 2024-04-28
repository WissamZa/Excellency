from django.shortcuts import render

# Create your views here.
def order_form(request):
   
    return render(request, 'service/Service-request-form.html')

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