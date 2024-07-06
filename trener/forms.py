from django import forms
from ckeditor.widgets import CKEditorWidget
from django.core.validators import URLValidator, FileExtensionValidator
from .models import Exercise, ExerciseType, ExerciseLanguage, Person
import hashlib
import os
from django.core.exceptions import ValidationError
import re


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
        validators=[FileExtensionValidator(['gif', 'png', 'jpg', 'jpeg'])]
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

    # def clean_image(self):
    #     file = self.cleaned_data.get('image', False)
    #     if file:
    #         return file
    #     return self.instance.image if self.instance else None

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


class MyTrainingForm:
    def __init__(self, request_post):
        self.errors = None
        self.title = request_post.get('title', '')
        self.training_type = request_post.get('training-type', '')
        self.visibility = request_post.get('visible-radio', '')

        self.exercises_ids = []
        self.exercises_tips = {}
        for key, value in request_post.items():
            split_key = key.split('-')
            if len(split_key) == 3 and split_key[0] == 'exercise':
                if split_key[1] == 'id':
                    self.exercises_ids.append(split_key[2])
                elif split_key[1] == 'tips':
                    self.exercises_tips[split_key[2]] = value

    def is_valid(self):
        self.errors = MyTrainingErrors()
        if len(self.title) > 100:
            self.errors.title = "Nazwa treningu jest za długa."
            self.errors.is_error = True

        if self.training_type not in ["general", "personal"]:
            self.errors.training_type = "Invalid training type"
            self.errors.is_error = True

        if self.visibility not in ["yes", "no"]:
            self.errors.visibility = "Invalid visibility type"
            self.errors.is_error = True

        general_exercise_ids = [str(exercise.id) for exercise in Exercise.objects.all()]

        for exercise_id in self.exercises_ids:
            if exercise_id not in general_exercise_ids:
                self.errors.exercise_id = "Exercise does not exist"
                self.errors.is_error = True

        return not self.errors.is_error


class MyTrainingErrors:
    def __init__(self):
        self.title = ""
        self.training_type = ""
        self.visibility = ""
        self.exercise_id = ""
        self.is_error = False



class ClientForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'photo', 'email', 'password', 'status', 'active_until']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
            'photo': forms.FileInput(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg file:bg-blue-50 file:border-blue-300 file:px-2.5 file:text-sm file:rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
            'password': forms.PasswordInput(attrs={'class': 'w-4/5 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
            'status': forms.Select(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5'}),
            'active_until': forms.DateInput(attrs={'class': 'w-full bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5', 'type': 'date'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if Person.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not re.match(r'^(?=.*\d)(?=.*[a-zA-Z]).{8,}$', password):
            raise ValidationError("Password must be at least 8 characters long and include at least one letter and one number.")
        return password

    def clean_photo(self):
        file = self.cleaned_data.get('photo', False)
        if file:
            md5 = hashlib.md5()
            for chunk in file.chunks():
                md5.update(chunk)
            file_hash = md5.hexdigest()

            extension = os.path.splitext(file.name)[1]
            new_name = f"{file_hash}{extension}"

            file.name = new_name
            return file


