from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from .forms import *

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    def post(self, request):
        return render(request, 'index.html')
    
class ConversaoView(View):
    def get(self, request):
        form = ArquivoForm()
        return render(request, 'conversao.html', {'form':form})
    def post(self, request):
        form = ArquivoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
        return render(request, 'conversao.html', {'form':form})