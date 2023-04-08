from django.shortcuts import render, redirect
from store.models import Product


def home(request):
    if request.user.is_authenticated:
        return redirect('okuu:learn_view', )
    else:
        return render(request, 'home.html',)



