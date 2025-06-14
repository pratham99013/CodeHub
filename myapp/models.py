from django.db import models
import uuid
# Create your models here.
from userapp.models import Profile

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete= models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null = True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default= "ilya-pavlov-OqtafYT5kTw-unsplash.jpg")
    demo_link = models.CharField(max_length=2000, null = True, blank=True)
    source_link = models.CharField(max_length=2000, null = True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    @property
    def reviewers(self):
        queryset = self.reviews.all().values_list('owner__id', flat=True)
        return queryset
    
    class Meta:
        ordering = ['-created']
    
    def getvotecount(self):
        reveiws = self.reviews.all()
        upvotes = reveiws.filter(value = 'up').count()
        total = reveiws.count()

        ratio = (upvotes/total)*100
        self.vote_total = total
        self.vote_ratio = ratio
        self.save()
    
    @property
    def imagURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''

        return url
    

    


class Review(models.Model):
    VOTE_TYPE = ( 
        ('up', 'UP Vote'),
        ('down' , 'down vote')
    )
    owner = models.ForeignKey(Profile, on_delete= models.CASCADE, null= True )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reviews")
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE) 
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    class Meta:
        unique_together = [['owner' , 'project']]

    def __str__(self):
        return self.value
    

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
