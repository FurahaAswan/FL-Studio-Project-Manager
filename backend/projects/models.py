from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=255)
    artists = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField()
    comments = models.TextField(null=True, blank=True)
    genre = models.CharField(max_length=100, null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True)
    path = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']
