from django.db import models
from AWS import create_folder

class ProjectManager(models.Manager):

    def create_by_aws(self, bucket, location,  directory_name):
        response = create_folder(bucket, directory_name)
        
        if response:
            return self.create(name=directory_name, key=response,
                                bucket=bucket, location=location)

class Project(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    key = models.CharField(max_length=100, null=False, blank=False)
    bucket = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='CREATED')

    objects = ProjectManager()

    def __str__(self):
        return self.name

    @property
    def items(self):
        return self.item_set.all()

    def uploading_file(self):
        self.status = 'UPLOADING FILE'
        self.save()

    def file_uploaded(self):
        self.status = 'FILE UPLOADED'
        self.save()

    def transcribe(self):
        self.status = 'TRANSCRIBE'

    def transcribed(self):
        self.status = 'TRANSCRIBED'