# Generated by Django 5.0.4 on 2024-05-15 10:50

import django.db.models.deletion
import trener.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseLanguage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('language_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralWorkout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalWorkout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('workout_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('short_description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=trener.models.exercise_directory_path)),
                ('video_link', models.URLField(blank=True, null=True)),
                ('html_content', models.TextField()),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trener.exerciselanguage')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trener.exercisetype')),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutExercise',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trener.exercise')),
                ('general_workout', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trener.generalworkout')),
                ('personal_workout', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trener.personalworkout')),
            ],
        ),
        migrations.AddField(
            model_name='personalworkout',
            name='exercises',
            field=models.ManyToManyField(through='trener.WorkoutExercise', to='trener.exercise'),
        ),
        migrations.AddField(
            model_name='generalworkout',
            name='exercises',
            field=models.ManyToManyField(through='trener.WorkoutExercise', to='trener.exercise'),
        ),
    ]