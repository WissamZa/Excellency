from django.http import HttpRequest
from django.shortcuts import render


def index_view(request: HttpRequest):
   return render(request, "main/index.html")
