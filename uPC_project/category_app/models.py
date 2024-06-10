# category_app/models.py

from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class Category(models.Model):
    Ct_IndexNumber = models.AutoField(primary_key=True)
    Ct_MajorName = models.CharField(max_length=10)
    Ct_MinorName = models.CharField(max_length=10)
    Ct_MajorNumber = models.IntegerField(choices=[(i, i) for i in range(1, 4)])
    Ct_MinorNumber = models.IntegerField(choices=[(i, i) for i in range(1, 9)])

    class Meta:
        db_table = 'category'

class CategoryProduct(models.Model):
    Pd_IndexNumber = models.AutoField(primary_key=True)
    Pd_Market = models.CharField(max_length=10)
    Pd_CategoryNumber = models.IntegerField(default=1)
    Pd_Category = models.CharField(max_length=50)
    Pd_Name = models.CharField(max_length=150, unique=True)
    Pd_Price = models.BigIntegerField()
    Pd_IMG = models.CharField(max_length=500)
    Pd_URL = models.CharField(max_length=300)
    Pd_Count = models.IntegerField(default=0)

    class Meta:
        db_table = 'CategoryProduct'

    def increase_popularity_count(self):
        self.Pd_Count += 1
        self.save()

    def decrease_popularity_count(self):
        if self.Pd_Count > 0:
            self.Pd_Count -= 1
            self.save()
        else:
            self.Pd_count = 0


@receiver(post_migrate)
def create_initial_records(sender, **kwargs):

    majorName = ['중고 완제품', '중고 PC 주요부품', '중고 PC 주변기기']
    minorName = ['중고 데스크탑', '중고 노트북', 'CPU', '메인보드', '메모리', '그래픽카드', 'SSD', 'HDD', '케이스', '파워', '키보드', '마우스', '모니터', '스피커/헤드셋']
    minorCount = [2, 8, 4]

    for i in range(len(majorName)):
        start_index = 0 if i == 0 else sum(minorCount[:i])
        end_index = start_index + minorCount[i]

        if (len(Category.objects.all()) <=12 ) :
            for j in range(start_index, end_index):
                minor_number = j - start_index + 1 
                Category.objects.create(
                    Ct_MajorName=majorName[i],
                    Ct_MinorName=minorName[j],
                    Ct_MajorNumber=i + 2,  
                    Ct_MinorNumber=minor_number
                )
            print("haha")
            print("Inserted record")





