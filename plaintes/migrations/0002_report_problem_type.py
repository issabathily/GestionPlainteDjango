# Generated by Django 5.1.5 on 2025-03-16 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plaintes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='problem_type',
            field=models.CharField(choices=[('waste', 'Déchets'), ('road', 'Routes endommagées'), ('water', "Coupures d'eau"), ('electricity', 'Problèmes électriques'), ('other', 'Autres')], default='other', max_length=20),
        ),
    ]
