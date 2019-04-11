# Generated by Django 2.1.3 on 2019-04-03 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190403_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acciones',
            name='departamento_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acciones', to='core.Departamento'),
        ),
        migrations.AlterField(
            model_name='acciones',
            name='estado_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acciones', to='core.Estado'),
        ),
        migrations.AlterField(
            model_name='acciones',
            name='financiacion_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acciones', to='core.Financiacion'),
        ),
        migrations.AlterField(
            model_name='acciones',
            name='localidad_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acciones', to='core.Localidad'),
        ),
        migrations.AlterField(
            model_name='acciones',
            name='municipio_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acciones', to='core.Municipio'),
        ),
        migrations.AlterField(
            model_name='acciones',
            name='organismo_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acciones', to='core.Organismo'),
        ),
    ]