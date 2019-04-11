# Generated by Django 2.1.3 on 2019-04-11 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20190411_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organismo',
            old_name='usuarios',
            new_name='usuario',
        ),
        migrations.AlterField(
            model_name='acciones',
            name='localidad_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acciones', to='core.Localidad'),
        ),
    ]
