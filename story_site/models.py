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


class Event(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(Region, unique=False)
    country = models.ForeignKey(Country, unique=False)
    city = models.ForeignKey(City, unique=False)
    def __unicode__(self):
        return self.name

class AudioFormat(models.Model):
    name = models.CharField(max_length=30)
    def __unicode__(self):
        return self.name

class OwnedAudioFile(models.Model):
    title = models.CharField(max_length=30)
    audioFormat = models.ForeignKey(AudioFormat, unique=False)
    filePath = models.CharField(max_length=500)
    webPath = models.CharField(max_length=500)
    duration = models.PositiveIntegerField()

    def __unicode__(self):
        return self.title


class Story(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    language = models.ForeignKey(Language, unique=False)
    country = models.ForeignKey(Country, unique=False)
    region = models.ForeignKey(Region, unique=False)
    dialect = models.ForeignKey(Dialect, unique=False)
    city = models.ForeignKey(City, unique=False)
    storyFile = models.ForeignKey(OwnedAudioFile, unique=False)
    owner = models.ForeignKey(User, unique=False)
    event = models.ForeignKey(Event, unique=False)
    averageRank = models.DecimalField(max_digits=5, decimal_places=3)
    numVotes = models.PositiveIntegerField()
    # durationSeconds = models.PositiveIntegerField()
    

    def __unicode__(self):
        return self.title





class Compilation(models.Model):
    timeCreated = models.DateTimeField()
    user = models.ForeignKey(User, unique=False)
    story = models.ManyToManyField(Story)
    averageRank = models.DecimalField(max_digits=5, decimal_places=3)
    numVotes = models.PositiveIntegerField()

    def __unicode__(self):
        return self.timeCreated


class PersonalCompilationRank(models.Model):
    rank = models.DecimalField(max_digits=5, decimal_places=3)
    compilation = models.ForeignKey(Compilation, unique=False)
    user = models.ForeignKey(User, unique=False)

    def __unicode__(self):
        return self.rank


class PersonalStoryRank(models.Model):
    rank = models.DecimalField(max_digits=5, decimal_places=3)
    story = models.ForeignKey(Story, unique=False)
    user = models.ForeignKey(User, unique=False)

    def __unicode__(self):
        return self.rank
    

class UserKind(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bio = models.CharField(max_length=1000)
    kind = models.ForeignKey(UserKind, unique=False)
    birthdate = models.DateField()
    country = models.ForeignKey(Country, unique=False)
    city = models.ForeignKey(City, unique=False)

    def __unicode__(self):
        return self.user.username


class Keywords(models.Model):
    name = models.CharField(max_length=75)
    story = models.ForeignKey(Story, unique=False)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=75)
    story = models.ForeignKey(Story, unique=False)

    def __unicode__(self):
        return self.name


class CompilationTag(models.Model):
    tag = models.ForeignKey(Tag, unique=False)
    compilation = models.ForeignKey(Compilation, unique=False)

    def __unicode__(self):
        return self.tag.name


class Review(models.Model):
    header = models.CharField(max_length=100)
    review = models.CharField(max_length=2000)
    stars = models.IntegerField()
    user = models.ForeignKey(User, unique=False)
    story = models.ForeignKey(Story, unique=False)

    def __unicode__(self):
        return self.header
