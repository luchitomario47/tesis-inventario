# Generated by Django 5.1 on 2024-10-22 20:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InvCab',
            fields=[
                ('id_inv', models.BigAutoField(primary_key=True, serialize=False)),
                ('store', models.CharField(max_length=3)),
                ('nota_inv', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.IntegerField(default=0)),
                ('estado_conteo', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('id_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InvConteo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zona', models.IntegerField()),
                ('cod_plano', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('id_inv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventarioApp.invcab')),
            ],
        ),
        migrations.CreateModel(
            name='InvDet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('zona', models.IntegerField()),
                ('sku', models.CharField(max_length=20)),
                ('linea', models.IntegerField()),
                ('modelo', models.CharField(max_length=13)),
                ('color', models.TextField()),
                ('talla', models.CharField(max_length=5)),
                ('descripcion', models.CharField(max_length=50)),
                ('temp_comercial', models.CharField(max_length=10)),
                ('familia', models.CharField(max_length=10)),
                ('marca', models.CharField(blank=True, max_length=10, null=True)),
                ('cantidad', models.IntegerField()),
                ('username', models.CharField(max_length=21)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('id_inv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventarioApp.invcab')),
            ],
        ),
    ]
