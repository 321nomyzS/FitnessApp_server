from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from ckeditor.widgets import CKEditorWidget
from .models import Exercise

class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['title', 'short_description', 'image', 'video_link', 'html_content']
        widgets = {
            'html_content': CKEditorWidget(),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            file_extension = image.name.split('.')[-1].lower()
            if file_extension not in ['gif', 'png', 'jpg', 'jpeg']:
                raise ValidationError("Zdjęcie musi być w formacie GIF, PNG lub JPG.")
        return image
