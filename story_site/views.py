from django.shortcuts import render, HttpResponse, render_to_response
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import UploadAudioFileForm, NoTitleSearchForm
from .models import OwnedAudioFile, Language, Region, Country, City, Dialect, Story, Event, Compilation, PersonalCompilationRank, PersonalStoryRank
from files import handle_uploaded_file, handle_compilation
from django.core.context_processors import csrf
from django.db.models import Q
from django.conf import settings
import os
import json
from datetime import datetime
from audioProcess import concatenate_audio_files
from .story_tools import compile_stories, most_frequent_tags
from populate_database import populate_countries, populate_users, populate_kinds, populate_audio_files, populate_languages




startWithNoneDict = { "language" : Language.objects.get(name = "None").id,
                      "region" : Region.objects.get(name = "None").id,
                      "country" : Country.objects.get(name = "None").id,
                      "city" : City.objects.get(name = "None").id,
                      "dialect" : Dialect.objects.get(name = "None").id,
                  }


def buildTestDb(request):
    # populate_kinds()
    # populate_users()
    # populate_audio_files()
    populate_languages()
    return HttpResponse("Done")

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
    # form = NoTitleSearchForm(initial = startWithNoneDict)
    # c = { "form" : form }
    # c.update(csrf(request))


    allLangs = Language.objects.order_by('name')
    allCountries = Country.objects.order_by('name')

    return render(request, 'story_site/compilation.html', {"languages" : allLangs, "countries" : allCountries})

def user_page(request):

    if not request.user.is_authenticated:
        return redirect('login_page')


    kindVar = "profile"
    if request.method == "GET":
        if "kind" in request.GET:
            kindVar = request.GET['kind']

        

    #TODO - Optimize so we don't load everything each time
    #TODO - Find a sensible way of limiting the number of compilations
    allCompilations = Compilation.objects.filter(user = request.user).order_by("-timeCreated")[:5]

    allAudio = Story.objects.filter(owner = request.user)

    # for compilation in allCompilations:
    #     for story in compilation.story.all():
    #         print story.title

    # form = UploadAudioFileForm(initial = startWithNoneDict)
    c = { "allAudio" : allAudio, "previousCompilations" : allCompilations, "kind" : kindVar}# , "form" : form }
    c.update(csrf(request))

    
    return render(request, 'story_site/userhome.html', c)


def upload_audio_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    


    allAudio = Story.objects.filter(owner = request.user)

    form = UploadAudioFileForm(initial = startWithNoneDict)
    c = { "allAudio" : allAudio, "form" : form }
    c.update(csrf(request))

    
    return render(request, 'story_site/upload_audio.html', c)
                      


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
            dialect = form.cleaned_data['dialect']
            # city = form.cleaned_data['city']
            city = City.objects.get(name="None")
            event = Event.objects.get(name="None")
            
            dbFile = handle_uploaded_file(request.FILES['file'], request.user, title, description, region, language, country, city, dialect, event)
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

        language = Language.objects.get(name=request.POST['language'])
        country = Country.objects.get(name=request.POST['country'])

        city = None
        if 'city' in request.POST:
            cityName = request.POST['city']
            if cityName != "None":
                city = City.objects.get(name=request.POST['city'], country=country)

            else:
                city = City.objects.get(name=request.POST['city'])
        
        
        tagsJson = request.POST['tags']
        tags = json.loads(tagsJson)

        duration = int(request.POST['duration'])
    

        
        # TODO: Fix bug - if there are no stories shorter than the length provided, includes all stories
        matchingAudioFiles = compile_stories(language, country, city, tags, duration*60)




        toCombine = []

        if matchingAudioFiles:
            for audio in matchingAudioFiles:
                toCombine.append(audio.storyFile.filePath)
                
        destPath = handle_compilation(toCombine, request.user.username)

        if destPath:
            compilation = Compilation(user = request.user, timeCreated = datetime.now(), averageRank = 0, numVotes = 0)
            compilation.save()

            bestTags = most_frequent_tags(10, matchingAudioFiles)

            for tag in bestTags:
                CompilationTag.objects.create(tag = tag, compilation = compilation)
            

            for story in matchingAudioFiles:
                compilation.story.add(story)
            compilation.save()


            request.session['destPath'] = destPath
            return redirect('compile_success')





    allLangs = Language.objects.order_by('name')
    allCountries = Country.objects.order_by('name')

    return render(request, 'story_site/compilation.html', {"noneFound" : True, "languages" : allLangs, "countries" : allCountries})




def get_cities_ajax(request):
    if request.method=="GET":
        country_name = request.GET['country']
        country = Country.objects.get(name=country_name)
        cities = City.objects.filter(country=country)

        htmlStr = "<select name='city' form='compile_form'>"
        htmlStr += "<option value='None'>All Cities</option>\n"
        for city in cities:
            htmlStr+="<option value='"+city.name+"'>"+city.name+"</option>\n"
        htmlStr+="</select>"

        
        return HttpResponse(htmlStr)
    return HttpResponse("")
        


def get_compilations_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login_page')


        
    if "pageNum" in request.GET:
        pageNum = int(request.GET['pageNum'])
    else:
        return HttpResponse("")
        
    allCompilations = Compilation.objects.filter(user = request.user).order_by("-timeCreated")[pageNum * 5: (pageNum * 5) + 5]

    print allCompilations

    
    htmlStr = """
    <h3> Compilation Title </h3>
    <table class="previous_compilation_table">
    <tr>
      <td>Tags: </td>
      <td>

      </td>
    </tr>
    
    <tr>
      <th> Title </th>
      <th> Description </th>
    </tr>
    """

    for x in [] :
        htmlStr += """
        <tr>
        <td>{{ story.title }}</td>
        <td>{{ story.description | truncatewords:10 }}</td>
        </tr>
        """
    htmlStr += """<tr><td></td><td><a href="#"> Read more... </a></td><td></td></tr>
    
    
  </table>

    """

    return HttpResponse(htmlStr)



def rank_compilation_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login_page')


    if "rank" in request.GET and "compilation_id" in request.GET:
        rank = int(request.GET['rank'])
        compilation_id = request.GET['compilation_id']
    else:
        return HttpResponse("")

    compilation = Compilation.objects.get(id=compilation_id)


    oldRank = PersonalCompilationRank.objects.filter( compilation = compilation, user = request.user)
    if oldRank.count() == 0:
        alreadyRanked = False
    else:
        alreadyRanked = True
        oldRankVal = oldRank[0].rank
    oldRank.delete()


    newCompilationRank = PersonalCompilationRank(user = request.user, compilation = compilation, rank = rank)
    newCompilationRank.save()

    if not alreadyRanked:
        currentAverageRankTotal = compilation.averageRank * compilation.numVotes
        newNumVotes = compilation.numVotes + 1
        
        newAverageRank = (currentAverageRankTotal + rank) / newNumVotes
        
        compilation.numVotes = newNumVotes
        compilation.averageRank = newAverageRank
        compilation.save()

    else:
        currentAverageRankTotal = compilation.averageRank * compilation.numVotes
        newAverageRankTotal = (currentAverageRankTotal - oldRankVal) + rank
        newAverageRank = newAverageRankTotal / compilation.numVotes
        compilation.averageRank = newAverageRank
        compilation.save()
    

    return HttpResponse("")







def rank_story_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login_page')


    if "rank" in request.GET and "story_id" in request.GET:
        rank = int(request.GET['rank'])
        story_id = request.GET['story_id']
    else:
        return HttpResponse("")

    story = Story.objects.get(id=story_id)



    oldRank = PersonalStoryRank.objects.filter( story = story, user = request.user)
    if oldRank.count() == 0:
        alreadyRanked = False
    else:
        alreadyRanked = True
        oldRankVal = oldRank[0].rank
    oldRank.delete()


    newStoryRank = PersonalStoryRank(user = request.user, story = story, rank = rank)
    newStoryRank.save()

    if not alreadyRanked:
        currentAverageRankTotal = story.averageRank * story.numVotes
        newNumVotes = story.numVotes + 1
        
        newAverageRank = (currentAverageRankTotal + rank) / newNumVotes
        
        story.numVotes = newNumVotes
        story.averageRank = newAverageRank
        story.save()

    else:
        print story.averageRank
        currentAverageRankTotal = story.averageRank * story.numVotes
        newAverageRankTotal = (currentAverageRankTotal - oldRankVal) + rank
        newAverageRank = newAverageRankTotal / story.numVotes
        print newAverageRank
        story.averageRank = newAverageRank
        story.save()


    

    return HttpResponse("")
