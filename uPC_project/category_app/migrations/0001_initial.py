# Generated by Django 4.2.10 on 2024-06-09 09:43

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("Ct_IndexNumber", models.AutoField(primary_key=True, serialize=False)),
                ("Ct_MajorName", models.CharField(max_length=10)),
                ("Ct_MinorName", models.CharField(max_length=10)),
                (
                    "Ct_MajorNumber",
                    models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)]),
                ),
                (
                    "Ct_MinorNumber",
                    models.IntegerField(
                        choices=[
                            (1, 1),
                            (2, 2),
                            (3, 3),
                            (4, 4),
                            (5, 5),
                            (6, 6),
                            (7, 7),
                            (8, 8),
                        ]
                    ),
                ),
            ],
            options={
                "db_table": "category",
            },
        ),
        migrations.CreateModel(
            name="CategoryProduct",
            fields=[
                ("Pd_IndexNumber", models.AutoField(primary_key=True, serialize=False)),
                ("Pd_Market", models.CharField(max_length=10)),
                ("Pd_CategoryNumber", models.IntegerField(default=1)),
                ("Pd_Category", models.CharField(max_length=50)),
                ("Pd_Name", models.CharField(max_length=150, unique=True)),
                ("Pd_Price", models.BigIntegerField()),
                ("Pd_IMG", models.CharField(max_length=500)),
                ("Pd_URL", models.CharField(max_length=300)),
                ("Pd_Count", models.IntegerField(default=0)),
            ],
            options={
                "db_table": "CategoryProduct",
            },
        ),
    ]
