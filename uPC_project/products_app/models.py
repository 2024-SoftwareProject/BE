from django.db import models

# Create your models here.

class Product(models.Model):
    Pd_IndexNumber = models.AutoField(primary_key=True)
    Pd_name = models.CharField(max_length=255)
    Pd_Price = models.IntegerField()
    Pd_IMG = models.CharField(max_length=500)
    Pd_Market = models.CharField(max_length=10)
    Pd_IMG = models.CharField(max_length=500)
    Pd_URL = models.CharField(max_length=300)

    class Meta:
        db_table = 'Product'