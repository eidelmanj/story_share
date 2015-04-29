from django.shortcuts import render, HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import IntegrityError

# Create your views here.
def index(request):
    return render(request, 'story_site/index.html', {})

    
def login_page(request):
    return render(request, 'story_site/login.html', {})

def authentication_page(request):
    if request.method == "POST":
        uName = request.POST.get("username_input")
        pWord = request.POST.get("password_input")
        user = authenticate(username=uName, password=pWord)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/story_site/')
            return redirect('/story_site/login_error.html')
        else:
            return redirect('/story_site/login_error.html')

    else:
        return redirect('/story_site/login_error.html')


def logout_page(request):
    logout(request)
    return redirect('/story_site/')


def register_page(request):
    print (str(request.session.get('userAlreadyTaken', False)))
    
    userAlreadyTaken = request.session.get('userAlreadyTaken', False)
    if 'userAlreadyTaken' in request.session:
        del request.session['userAlreadyTaken']
        
    request.session.modified = True
    
    return render(request, 'story_site/register.html', {"userAlreadyTaken" : userAlreadyTaken})


def generate_user(request):
    if request.method == "POST":
        uName = request.POST.get("username_input")
        pWord = request.POST.get("password_input")
        email = request.POST.get("email_input")

        if uName and pWord and email:
            try: 
                user = User.objects.create_user(uName, email, pWord)
            except IntegrityError:
                request.session['userAlreadyTaken'] = True
                return redirect('register_page')
                
            if user:
                print user.username
                return redirect('/story_site/')
            else:
                return redirect('/story_site/register/')

        else:
            return redirect('/story_site/register_error/')

    else:
        return redirect('/story_site/register_error/')
            
