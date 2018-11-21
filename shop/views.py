from django.shortcuts import render, HttpResponse
from django.utils import timezone


def test(request):
    time = timezone.now()
    return HttpResponse("<p>The time now is: {}</p>".format(time))
