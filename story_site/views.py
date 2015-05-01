from django.shortcuts import render, HttpResponse, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import UploadAudioFileForm, NoTitleSearchForm
from .models import OwnedAudioFile, Language, Region, Country
from files import handle_uploaded_file, handle_compilation
from django.core.context_processors import csrf
from django.db.models import Q
from django.conf import settings
import os
from audioProcess import concatenate_audio_files




startWithNoneDict = { "language" : Language.objects.get(name = "None").id,
                      "region" : Region.objects.get(name = "None").id,
                      "country" : Country.objects.get(name = "None").id,
                  }


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


def logout_page(request):
    logout(request)
    return redirect('index')


def register_page(request):
    userAlreadyTaken = request.session.get('userAlreadyTaken', False)
    if 'userAlreadyTaken' in request.session:
        del request.session['userAlreadyTaken']
        
    request.session.modified = True
    
    return render(request, 'story_site/register.html', {"userAlreadyTaken" : userAlreadyTaken})

def compilation_page(request):
    form = NoTitleSearchForm(initial = startWithNoneDict)
    c = { "form" : form }
    c.update(csrf(request))

    return render(request, 'story_site/compilation.html', c)

def user_page(request):

    if not request.user.is_authenticated:
        return redirect('login_page')
    


    allAudio = OwnedAudioFile.objects.filter(owner = request.user)

    form = UploadAudioFileForm()
    c = { "allAudio" : allAudio, "form" : form }
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


    return redirect('register_error')
            


def upload_file(request):

    if not request.user.is_authenticated:
        return redirect('login_page')

    
    
    if request.method=="POST":
        form = UploadAudioFileForm(request.POST, request.FILES)
        if form.is_valid():

            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            language = form.cleaned_data['language']
            region = form.cleaned_data['region']
            country = form.cleaned_data['country']
            
            dbFile = handle_uploaded_file(request.FILES['file'], request.user, title, description, region, language, country )
            if not dbFile:
                redirect('upload_error')
                
            return redirect('user_page')

    return redirect('index')


def compile_success(request):
    destPath = request.session['destPath']


    if 'destPath' in request.session:
        del request.session['destPath']
        
    request.session.modified = True

    if not destPath:
        return redirect('error')
    
    return render(request, 'story_site/compile_success.html', {"destPath" : destPath})


def generate_compiled_stories(request):
    if not request.user.is_authenticated:
        return redirect('login_page')

    if request.method=="POST":
        form = NoTitleSearchForm(request.POST, request.FILES)
        if form.is_valid():
            language = form.cleaned_data['language']
            region = form.cleaned_data['region']
            country = form.cleaned_data['country']

            matchingAudioFiles = OwnedAudioFile.objects.filter( Q(region=region) | Q(region=Region.objects.get(name = "None").id),
                                                                Q(country=country) | Q(country=Country.objects.get(name = "None").id),
                                                                Q(language=language) | Q(language=Language.objects.get(name = "None").id))

            toCombine = []
            for audio in matchingAudioFiles:
                toCombine.append(audio.filePath)
                
            destPath = handle_compilation(toCombine, request.user.username)

            if destPath:
                request.session['destPath'] = destPath
                return redirect('compile_success')





        
    return redirect('compile_error')
