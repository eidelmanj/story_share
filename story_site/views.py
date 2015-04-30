from django.shortcuts import render, HttpResponse, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import UploadAudioFileForm
from files import handle_uploaded_file
from django.core.context_processors import csrf

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
                return redirect('index')
            return redirect('login_error')
        else:
            return redirect('login_error')

    else:
        return redirect('login_error')


def logout_page(request):
    logout(request)
    return redirect('index')


def register_page(request):
    print (str(request.session.get('userAlreadyTaken', False)))
    
    userAlreadyTaken = request.session.get('userAlreadyTaken', False)
    if 'userAlreadyTaken' in request.session:
        del request.session['userAlreadyTaken']
        
    request.session.modified = True
    
    return render(request, 'story_site/register.html', {"userAlreadyTaken" : userAlreadyTaken})

def user_page(request):
    form = UploadAudioFileForm()
    c = { "form" : form }
    c.update(csrf(request))
    return render(request, 'story_site/userhome.html', c)


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
                return redirect('index')
            else:
                return redirect('register_page')

        else:
            return redirect('register_error')

    else:
        return redirect('register_error')
            


def upload_file(request):

    if not request.user.is_authenticated:
        return redirect('login_page')

    
    
    if request.method=="POST":
        form = UploadAudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            # print str(request.FILES.keys())
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            
            handle_uploaded_file(request.FILES['file'], request.user, title, description )
            return redirect('user_page')

    return redirect('index')
