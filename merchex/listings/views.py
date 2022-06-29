from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse('<h1>Hello Django!</h1>')


def about(request):
    return HttpResponse('<h1>About Us</h1> <p>We love merch!</p>')


def contact(request):
    return HttpResponse('<h1>Contact Us</h1> <p>Mail :</p>')


def listings(request):
    return HttpResponse('<h1>Liste de course</h1> <p>PQ</p>')
