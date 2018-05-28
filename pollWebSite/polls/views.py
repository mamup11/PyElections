from django.shortcuts import render
from .backend import Menu

def index(request):
    candidatos = Menu.fillDto()
    context = {'candidato': candidatos[0]}
    return render(request, 'index.html', context)