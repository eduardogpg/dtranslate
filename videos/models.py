from django.db import models

from .constants import STATUS
from .constants import UPLOAD, TRANSCRIBE, TRANSLATE, SUBTITLE, COMPLETED

class VideoManager(models.Manager):
    pass

class Video(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    content_type = models.CharField(max_length=10, null=False, blank=False)
    key = models.CharField(max_length=200)
    bucket = models.CharField(max_length=50, null=False, blank=False)
    location = models.CharField(max_length=20, null=False, blank=False)
    status = models.IntegerField(choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def upload(self):
        self.status = UPLOAD
        self.save()

    def transcribe(self):
        self.status = TRANSCRIBE
        self.save()
    
    def translate(self):
        self.status = TRANSLATE
        self.save()

    def subtitle(self):
        self.status = SUBTITLE
        self.save()

    def completed(self):
        self.status = COMPLETED
        self.save()

    def set_key(self, key):
        self.key = key
        self.save()

    @property
    def url(self):
        return f"https://s3-{self.location}.amazonaws.com/{self.bucket}/{self.key}"
        
    @property
    def format(self):
        return self.content_type.split('/')[-1]

    @property
    def name(self):
        return self.title.split('.')[0].lower().replace(' ', '_')