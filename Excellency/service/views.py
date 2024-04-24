from django.shortcuts import render

# Create your views here.
def order_form(request):
   
    return render(request, 'service/Service-request-form.html')

def payment_view(request):
    return render(request, 'service/payment.html')

def chat_view(request):
    return render(request, 'service/chat.html')