from django.db import migrations

def create_sample_plants(apps, schema_editor):
    Plant = apps.get_model('trener', 'Plant')
    WaterNeed = apps.get_model('trener', 'WaterNeed')
    LightRequirement = apps.get_model('trener', 'LightRequirement')
    CareLevel = apps.get_model('trener', 'CareLevel')

    # Pobranie istniejących danych (lub dodanie nowych, jeśli ich nie ma)
    water_low = WaterNeed.objects.get_or_create(name='Niewielka', description='Podlewanie rzadko, co 2-3 tygodnie')[0]
    light_medium = LightRequirement.objects.get_or_create(name='Umiarkowane światło', description='Jasne, ale pośrednie światło')[0]
    care_easy = CareLevel.objects.get_or_create(name='Niska pielęgnacja', description='Wymaga minimalnej pielęgnacji')[0]

    # Tworzenie przykładowych roślin
    Plant.objects.create(
        name='Fikus',
        description='Roślina doniczkowa idealna do wnętrz',
        image='path/to/fikus.jpg',
        water_need=water_low,
        light_requirement=light_medium,
        care_level=care_easy,
        is_indoor=True
    )

    Plant.objects.create(
        name='Monstera',
        description='Roślina doniczkowa o dużych liściach',
        image='path/to/monstera.jpg',
        water_need=water_low,
        light_requirement=light_medium,
        care_level=care_easy,
        is_indoor=True
    )


class Migration(migrations.Migration):

    dependencies = [
        ('trener', '0007_auto_20240905_0126'),
    ]

    operations = [
        migrations.RunPython(create_sample_plants),
    ]
