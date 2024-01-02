from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField()
    project_file = models.FileField(upload_to='project_files/')

    def __str__(self):
        return self.name
