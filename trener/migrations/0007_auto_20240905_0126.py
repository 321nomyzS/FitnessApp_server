from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('trener', '0006_auto_20240905_0125'),  # zamień na rzeczywistą nazwę ostatniej migracji
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='water_need',
            field=models.ForeignKey(on_delete=models.CASCADE, to='trener.WaterNeed'),
        ),
    ]
