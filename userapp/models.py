from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
# Create your models here.
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    short_intro = models.CharField(max_length=500, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='ali-mammadli-ngAuVVO1lQ4-unsplash.jpg')
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ['-created']
    
    @property
    def imagURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''

        return url
    
    



class Skills(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
    

# @receiver(post_save, sender = Profile)
def createUpdate(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email= user.email,
            name = user.first_name

        )



post_save.connect(createUpdate, sender=User)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete= models.SET_NULL, null=True,  related_name='sent_messages' )
    recepient = models.ForeignKey(Profile, on_delete= models.SET_NULL, null=True,  related_name='messages' )
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
         ordering = ['is_read' , '-created']

    def __str__(self):

        return str(self.name)
