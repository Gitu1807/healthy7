from django.contrib.auth.models import AbstractUser , User

from django.db import models

# Create your models here.
# Product Info Here 
class product(models.Model):
    CAT=((1,'Personal Care'),(2,'Health Care Devices'),(3,'Skin Care'),(4,'Fitness Supplement'),(5,'Ayurvedic Care'),(6,'Health Care'))
    name=models.CharField(max_length=100 ,verbose_name='Product Name')
    price=models.FloatField()
    cat=models.IntegerField(max_length=50, verbose_name='Category' ,choices=CAT)
    cdetail=models.CharField(max_length=300, verbose_name='Product Detail')
    cimage=models.ImageField(upload_to='image')
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE, db_column='pid')
    qty=models.IntegerField(default=1)

class Order(models.Model):
    orderid=models.IntegerField()
    uid=models.ForeignKey('auth.User',on_delete=models.CASCADE, db_column='uid')
    pid=models.ForeignKey('Product',on_delete=models.CASCADE, db_column='pid')
    qty=models.IntegerField(default=1)
    amount=models.FloatField()

# Product Info eND Here 


    

    

