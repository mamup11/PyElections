from django.shortcuts import render
from .backend import Menu

Menu.fillDto()

def index(request):
    candidatos = Menu.getDto()
    context = {'candidatos': candidatos}
    return render(request, 'index.html', context)
