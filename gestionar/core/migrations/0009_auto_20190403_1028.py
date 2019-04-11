# Generated by Django 2.1.3 on 2019-04-03 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190401_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='acciones',
            name='importancia',
            field=models.IntegerField(choices=[('1', 'Prioritaria'), ('3', 'Intermedia'), ('6', 'Leve'), ('9', 'Sin Marcar')], default=9),
        ),
        migrations.AlterField(
            model_name='acciones',
            name='localidad_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Localidad'),
        ),
    ]
