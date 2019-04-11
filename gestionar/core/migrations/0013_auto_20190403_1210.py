# Generated by Django 2.1.3 on 2019-04-03 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20190403_1150'),
    ]

    operations = [
        migrations.RenameField(
            model_name='acciones',
            old_name='organismo_id',
            new_name='organismo_ws',
        ),
        migrations.AlterField(
            model_name='acciones',
            name='localidad_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acciones', to='core.Localidad'),
        ),
    ]
