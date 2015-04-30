from django.db import models
from django.contrib.auth.models import User

# Create your models here.

### Useless model that I can't seem to get rid of without breaking things
class AudioFile(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, unique=False)
    filePath = models.CharField(max_length=500)


class OwnedAudioFile(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, unique=False)
    filePath = models.CharField(max_length=500)
