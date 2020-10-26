from django.db import models

from projects.models import Project

class Item(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    key = models.CharField(max_length=200, null=True, blank=True)
    bucket = models.CharField(max_length=100, null=True, blank=True)
    content_type = models.CharField(max_length=100, null=False, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    lenguage = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name

    @property
    def format(self):
        return self.content_type.split('/')[1]

    @property
    def uri(self):
        return f"https://s3-{self.project.location}.amazonaws.com/{self.bucket}/{self.key}"
