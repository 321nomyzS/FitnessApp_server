from django import forms
from ckeditor.widgets import CKEditorWidget
from django.core.validators import URLValidator, FileExtensionValidator
from .models import Exercise, ExerciseType, ExerciseLanguage
import hashlib
from django.core.files.uploadedfile import InMemoryUploadedFile
import os


class ExerciseForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
        label="Nazwa ćwiczenia",
        max_length=100
    )
    short_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full block p-1.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500', 'rows': 4}),
        label="Krótki opis"
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'id': 'dropzone-file', 'class': 'hidden'}),
        label="Zdjęcie lub GIF",
        validators=[FileExtensionValidator(['gif', 'png', 'jpg', 'jpeg'])]  # Dodajemy walidator dla rozszerzenia pliku
    )
    video_link = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
        label="Link do wideo",
        validators=[URLValidator()]  # Dodajemy walidator URL
    )
    html_content = forms.CharField(
        widget=CKEditorWidget(),
        label="Długi opis"
    )

    type_choices = [(type_obj.id, type_obj.type_name) for type_obj in ExerciseType.objects.all()]
    language_choices = [(language_obj.id, language_obj.language_name) for language_obj in ExerciseLanguage.objects.all()]

    type = forms.ChoiceField(
        choices=type_choices,
        widget=forms.Select(attrs={
            'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
        label="Typ ćwiczenia"
    )

    language = forms.ChoiceField(
        choices=language_choices,
        widget=forms.Select(attrs={
            'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
        label="Język"
    )

    def clean_type(self):
        type_id = self.cleaned_data.get('type')
        try:
            return ExerciseType.objects.get(id=type_id)
        except ExerciseType.DoesNotExist:
            raise forms.ValidationError("Type does not exist")

    def clean_language(self):
        language_id = self.cleaned_data.get('language')
        try:
            return ExerciseLanguage.objects.get(id=language_id)
        except ExerciseLanguage.DoesNotExist:
            raise forms.ValidationError("Language does not exist")

    def clean_image(self):
        file = self.cleaned_data.get('image', False)
        if file:
            md5 = hashlib.md5()
            for chunk in file.chunks():
                md5.update(chunk)
            file_hash = md5.hexdigest()

            extension = os.path.splitext(file.name)[1]
            new_name = f"{file_hash}{extension}"

            file.name = new_name
            return file
        else:
            raise forms.ValidationError("No file uploaded.")


    class Meta:
        model = Exercise
        fields = ['title', 'type', 'language', 'short_description', 'image', 'video_link', 'html_content']