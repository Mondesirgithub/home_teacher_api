# Generated by Django 4.1.7 on 2023-04-10 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0009_eleve_matieres'),
    ]

    operations = [
        migrations.AddField(
            model_name='eleve',
            name='jours_disponibles',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='eleve',
            name='periode_journee',
            field=models.CharField(default='', max_length=50),
        ),
    ]