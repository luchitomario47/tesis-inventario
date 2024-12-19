# Generated by Django 5.1 on 2024-12-19 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioApp', '0003_remove_productosrtpro_date_created_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='repositorioVentas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('invc_sid', models.CharField(max_length=50)),
                ('service_uid', models.CharField(max_length=50)),
                ('invoice_number', models.CharField(max_length=50)),
                ('createtime', models.DateTimeField()),
                ('channel', models.CharField(max_length=50)),
                ('sku', models.CharField(max_length=50)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
