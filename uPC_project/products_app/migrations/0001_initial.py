# Generated by Django 5.0.1 on 2024-05-13 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('Pd_IndexNumber', models.AutoField(primary_key=True, serialize=False)),
                ('Pd_Market', models.CharField(max_length=10)),
                ('Pd_Category', models.CharField(max_length=50)),
                ('Pd_Name', models.CharField(max_length=150, unique=True)),
                ('Pd_Price', models.BigIntegerField()),
                ('Pd_IMG', models.CharField(max_length=500)),
                ('Pd_URL', models.CharField(max_length=300)),
                ('Pd_Count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]
