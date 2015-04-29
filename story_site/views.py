from django.shortcuts import render, HttpResponse
from django.template import RequestContext, loader


# Create your views here.
def index(request):
    return render(request, 'story_site/index.html', {})

