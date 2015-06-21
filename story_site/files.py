import string
import random
import os
import utilities
from django.contrib.auth.models import User
from .models import OwnedAudioFile, Dialect, City, Story, AudioFormat
import audioProcess
from django.conf import settings




SAVE_TO = os.path.join(settings.MEDIA_ROOT, "user_files/")
TMP_DIR_PATH = os.path.join(settings.MEDIA_ROOT, "tmp/")


def handle_compilation(toCompile, username):

    userTmpDir = os.path.join(TMP_DIR_PATH, username)
    destFilePath = os.path.join(userTmpDir, "compiled_audio.mp3")

    
    if not os.path.exists(userTmpDir):
        os.makedirs(userTmpDir)

    

    return audioProcess.concatenate_audio_files(toCompile, userTmpDir)
    



def handle_uploaded_file(f, ownerUser, title, description, region, language, country, city, dialect, event):

    randomCode = utilities.id_generator(size=10)

    ownerUName = ownerUser.username

    #If the owner of this file doesn't have their own directory
    #in storage, create one
    if not os.path.exists(SAVE_TO + ownerUName):
        os.makedirs(SAVE_TO + ownerUName)

        
    filePath = SAVE_TO +  ownerUName + "/" + randomCode

    #Just in case we accidentally reuse the same file name, we
    #loop until we've found a new one
    while os.path.exists(filePath):
        randomCode = utilities.id_generator(size=10)
        filePath = SAVE_TO + ownerUName + "/" + randomCode


    #Write the file to storage
    with open(filePath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


    #Check the audio format of the file
    audioFormat = audioProcess.check_file_format(filePath)

    

    #If we have something that isn't an audio file, this is illegal
    if not audioFormat:
        os.remove(filePath)
        return None

    #Otherwise, add the appropriate extension to the filename
    else:
        print "at the else..."
        os.rename(filePath, filePath + "." +  audioFormat)

    formatEntry = AudioFormat.objects.get(name = audioFormat)

    a = OwnedAudioFile(filePath = filePath + "." +  audioFormat, audioFormat = formatEntry, title=title)
    a.save()
    s = Story(title = title, owner = ownerUser, description = description, language = language, region = region, country = country, dialect = dialect, city = city, storyFile = a, event=event)
    s.save()

    return a
    
