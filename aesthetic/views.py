from django.shortcuts import render
from .models import Aesthetic

# Create your views here.
def aesthetics_list(request):
  aesthetics = Aesthetic.objects.all().order_by('-date')
  return render(request, 'aesthetics/aesthetics_list.html',{'aesthetics':aesthetics})

def aesthetic_page(request,slug):
  aesthetic = Aesthetic.objects.get(slug=slug)
  return render(request,'aesthetics/aesthetic_page.html',{'aesthetic':aesthetic})
