from django.shortcuts import render, HttpResponse
from django.utils import timezone


def test(request):
    return render(request, 'base.html')
