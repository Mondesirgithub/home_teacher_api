# Generated by Django 4.1.7 on 2023-04-08 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comptes', '0006_alter_eleve_idtuteur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='telephone1',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]