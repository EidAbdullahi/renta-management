from django.shortcuts import render
from .models import Freelancer

def freelancer_list(request):
    freelancers = Freelancer.objects.all()
    return render(request, 'freelancers/list.html', {'freelancers': freelancers})
