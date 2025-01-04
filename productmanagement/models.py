from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.BigIntegerField()
    
    @classmethod   
    def get_product(cls):
        return cls.objects.first()
    
    def __str__(self):
        return self.name
    
