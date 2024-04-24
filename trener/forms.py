from django import forms
from django.forms import TextInput, Textarea, FileInput
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget
from .models import Exercise, ExerciseType, ExerciseLanguage


class ExerciseForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
        label="Nazwa ćwiczenia"
    )
    short_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'w-full block p-1.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500', 'rows': 4}),
        label="Krótki opis"
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={'id': 'dropzone-file', 'class': 'hidden'}),
        label="Zdjęcie lub GIF"
    )
    video_link = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
        label="Link do wideo"
    )
    html_content = forms.CharField(
        widget=CKEditorWidget(),
        label="Długi opis"
    )

    type_choices = [(type_obj.type_code, type_obj.type_name) for type_obj in ExerciseType.objects.all()]
    language_choices = [(language_obj.language_code, language_obj.language_name) for language_obj in ExerciseLanguage.objects.all()]

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

    class Meta:
        model = Exercise
        fields = ['title', 'short_description', 'image', 'video_link', 'html_content']

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            file_extension = image.name.split('.')[-1].lower()
            if file_extension not in ['gif', 'png', 'jpg', 'jpeg']:
                raise ValidationError("Zdjęcie musi być w formacie GIF, PNG lub JPG.")
        return image
