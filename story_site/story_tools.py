from .models import Language, City, Country, Tag, Story
from django.db.models import Q

def compile_stories(language, country, city, tags, duration):
    qLanguage = Q()
    if language.name != "None":
        qLanguage = Q(language = language)


    qCountry = Q()
    if country.name != "None":
        qCountry = Q(country = country)


    qCity = Q()
    if city and city.name != "None":
        qCity = Q(city = city)

    qTag = Q()
    for tag in tags:
        qTag = qTag | Q(tag__name=tag)


    qDuration = Q(storyFile__duration__lt=int(duration))

    matchingAudioFile = Story.objects.filter(qLanguage, qCountry, qCity, qTag, qDuration)[:100]

    allStories = matchingAudioFile

    totalDuration = 0
    qRemoveExtra = Q()
    i = 0

    while i<len(allStories) and int(totalDuration)<int(duration):        
        qRemoveExtra = qRemoveExtra | Q(title = allStories[i].title)
        totalDuration += allStories[i].storyFile.duration
        i+=1

    matchingAudioFile = Story.objects.filter(qRemoveExtra)
    
    return matchingAudioFile
        


def most_frequent_tags(n, storyList):
    # TODO
    return []
    

