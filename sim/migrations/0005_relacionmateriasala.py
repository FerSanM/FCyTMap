# Generated by Django 4.2.11 on 2024-03-20 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0004_rename_descripcion_actividades_descripcion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelacionMateriaSala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_entrada', models.TimeField()),
                ('hora_salida', models.TimeField()),
                ('dia_semana', models.CharField(choices=[('Lunes', 'Lunes'), ('Martes', 'Martes'), ('Miércoles', 'Miércoles'), ('Jueves', 'Jueves'), ('Viernes', 'Viernes'), ('Sábado', 'Sábado'), ('Domingo', 'Domingo')], max_length=10)),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sim.materia')),
                ('sala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sim.sala')),
            ],
        ),
    ]
