from django.http import JsonResponse
from django.shortcuts import render


def get_current_usd(request):
    return render(request, "currency/index.html")


def health_check(request):
    return JsonResponse({"status": "healthy"})
