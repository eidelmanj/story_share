import string
import random
import os
from django.contrib.auth.models import User
from .models import OwnedAudioFile


SAVE_TO = "/Users/jonathaneidelman/Dropbox/dev_projects/story_share/storage/"



def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def handle_uploaded_file(f, ownerUser, title, description):

    randomCode = id_generator(size=10)

    id_generator()
    print ownerUser.username
    ownerUName = ownerUser.username

    if not os.path.exists(SAVE_TO + ownerUName):
        os.makedirs(SAVE_TO + ownerUName)

    filePath = SAVE_TO +  ownerUName + "/" + randomCode + ".pdf"

    while os.path.exists(filePath):
        randomCode = id_generator(size=10)
        filePath = SAVE_TO + ownerUName + "/" + randomCode + ".pdf"

    a = OwnedAudioFile(owner = ownerUser, filePath = filePath, title=title, description = description )
    a.save()
    
    with open(filePath, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
