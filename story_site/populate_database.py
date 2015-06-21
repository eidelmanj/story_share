import json
import random
from os import listdir, path
from datetime import datetime
from .models import Country, City, Region, UserKind, UserProfile, Language, OwnedAudioFile, Story, Dialect, Event, AudioFormat
import utilities
from django.contrib.auth.models import User
from django.db.models import Q


NUM_USERS = 100

FILE_PATH = "/Users/jonathaneidelman/Dropbox/dev_projects/story_share/story_share/storage/user_files/test100/"

LORUM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

def populate_countries():
    with open("/Users/jonathaneidelman/Dropbox/dev_projects/story_share/story_share/story_site/test_db/countriesToCities2.json", "rb") as source:
        contents = json.load(source)
    



    Country.objects.filter(~Q(name="None")).delete()
    
    City.objects.filter(~Q(name="None")).delete()


    for country in contents:
        if not country=="":
            c = Country.objects.create(name=country)
            print contents[country]
            for city in contents[country]:
                cityName = (city[:47] + "..") if len(city)>47 else city
                City.objects.create(name=cityName, region=Region.objects.get(name="None"), country=c)
                


def populate_languages():
    with open("/Users/jonathaneidelman/Dropbox/dev_projects/story_share/story_share/story_site/test_db/countries_with_langs.json", 'rb') as source:
        contents = json.load(source)

    for country in contents:
        for language in country['languages']:
            test = Language.objects.filter(name=country['languages'][language].encode('ascii', 'ignore'))
            if not test:
                Language.objects.create(name=(country['languages'][language].encode('ascii', 'ignore')))




def populate_kinds():
    UserKind.objects.all().delete()
    UserKind.objects.create(name="individual")
    UserKind.objects.create(name="company")




def populate_users():
    # User.objects.filter(~Q(username="admin")).delete()
    
    allKinds = UserKind.objects.all()
    numKinds = UserKind.objects.count() - 1

    allCountries = Country.objects.all()
    numCountries = Country.objects.count() - 1

    allCities = City.objects.all()
    numCities = City.objects.count() - 1
    
    for i in range(1,NUM_USERS):
        rKind = random.randint(0, numKinds)
        rCountry = random.randint(0, numCountries)
        rCity = random.randint(0, numCities)
        
        u = User.objects.create_user(username="test"+str(i), email = "test"+str(i)+"@eidelman.com", password="test"+str(i))
        up = UserProfile.objects.create(user = u, bio = LORUM, kind=allKinds[rKind], birthdate = datetime.today(), country = allCountries[rCountry], city = allCities[rCity])




def populate_audio_files():
    allUsers = User.objects.all()

    allMusicFiles = listdir(FILE_PATH)

    allLangs = Language.objects.all()
    numLangs = Language.objects.count() - 1

    allCountries = Country.objects.all()
    numCountries = Country.objects.count() - 1

    allRegions = Region.objects.all()
    numRegions = Region.objects.count() - 1

    allDialects = Dialect.objects.all()
    numDialects = Dialect.objects.count() - 1

    allCities = City.objects.all()
    numCities = City.objects.count() - 1

    allEvents = Event.objects.all()
    numEvents = Event.objects.count() - 1
    

    for u in allUsers:
        r = random.randint(0, 50)
        for i in range(0, r):
            rFile = random.randint(0, len(allMusicFiles)-1)
            rLang = random.randint(0, numLangs)
            rCountry = random.randint(0, numCountries)
            rRegion = random.randint(0, numRegions)
            rDialect = random.randint(0, numDialects)
            rCity = random.randint(0, numCities)
            rEvent = random.randint(0, numEvents)
            

            lang = allLangs[rLang]
            country = allCountries[rCountry]
            region = allRegions[rRegion]
            dialect = allDialects[rDialect]
            city = allCities[rCity]
            event = allEvents[rEvent]

            
            title = utilities.id_generator(size=5)
            a = OwnedAudioFile.objects.create(title = title, audioFormat=AudioFormat.objects.get(name="mp3"), filePath = path.join(FILE_PATH, allMusicFiles[rFile]), webPath = "")

            s = Story.objects.create(title = title, description = LORUM, language=lang, country=country, region = region, dialect=dialect, city=city, event=event, owner=u, storyFile=a)
            

        
