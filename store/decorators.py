from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_page')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
