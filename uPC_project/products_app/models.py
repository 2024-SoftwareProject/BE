from django.db import models
from category_app.models import Category

class Product(models.Model):
    Pd_IndexNumber = models.AutoField(primary_key=True)
    Pd_Market = models.CharField(max_length=10)
    Pd_Category = models.CharField(max_length=50)
    Pd_Name = models.CharField(max_length=150, unique=True)
    Pd_Price = models.BigIntegerField()
    Pd_IMG = models.CharField(max_length=500)
    Pd_URL = models.CharField(max_length=300)
    Pd_Count = models.IntegerField(default=0)

    class Meta:
        db_table = 'product'

    def increase_popularity_count(self):
        self.Pd_Count += 1
        self.save()

    def decrease_popularity_count(self):
        if self.Pd_Count > 0:
            self.Pd_Count -= 1
            self.save()
        else:
            self.Pd_count = 0

