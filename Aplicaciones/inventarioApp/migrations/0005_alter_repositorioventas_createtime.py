# Generated by Django 5.1 on 2024-12-19 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioApp', '0004_repositorioventas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repositorioventas',
            name='createtime',
            field=models.DateField(),
        ),
    ]
