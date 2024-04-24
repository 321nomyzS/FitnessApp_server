from django.db import models
from django.core.validators import FileExtensionValidator


class ExerciseType(models.Model):
    id = models.AutoField(primary_key=True)
    type_code = models.CharField(max_length=3, unique=True)
    type_name = models.CharField(max_length=100)

    def __str__(self):
        return self.type_name


class ExerciseLanguage(models.Model):
    id = models.AutoField(primary_key=True)
    language_code = models.CharField(max_length=2, unique=True)
    language_name = models.CharField(max_length=50)

    def __str__(self):
        return self.language_name


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    short_description = models.TextField()
    image = models.ImageField(upload_to='exercise_images/', blank=True, null=True, validators=[FileExtensionValidator(['gif', 'png', 'jpg', 'jpeg'])])
    video_link = models.URLField(blank=True, null=True)
    html_content = models.TextField()
    type = models.ForeignKey(ExerciseType, on_delete=models.CASCADE)
    language = models.ForeignKey(ExerciseLanguage, on_delete=models.CASCADE)

    def __str__(self):
        return self.title