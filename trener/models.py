from django.db import models
from django.core.validators import FileExtensionValidator

class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    image = models.ImageField(upload_to='exercise_images/', blank=True, null=True, validators=[FileExtensionValidator(['gif', 'png', 'jpg', 'jpeg'])])
    video_link = models.URLField(blank=True, null=True)
    html_content = models.TextField()

    def __str__(self):
        return self.title
