# Generated by Django 4.2.11 on 2024-03-25 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0007_alter_relacionmateriasala_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='materia',
            options={'ordering': ['descripcion']},
        ),
    ]
