from django.db import models
from django.contrib.auth.models import User

# Create your models here.

### Useless model that I can't seem to get rid of without breaking things
class AudioFile(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(User, unique=False)
    filePath = models.CharField(max_length=500)
###################################



class Language(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    

class Dialect(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    

class Region(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, unique=False)

    def __unicode__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region, unique=False)
    country = models.ForeignKey(Country, unique=False)

    def __unicode__(self):
        return self.name


class OwnedAudioFile(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    language = models.ForeignKey(Language, unique=False)
    country = models.ForeignKey(Country, unique=False)
    region = models.ForeignKey(Region, unique=False)
    dialect = models.ForeignKey(Dialect, unique=False)
    city = models.ForeignKey(City, unique=False)
    owner = models.ForeignKey(User, unique=False)
    filePath = models.CharField(max_length=500)
    webPath = models.CharField(max_length=500)

    def __unicode__(self):
        return self.title
