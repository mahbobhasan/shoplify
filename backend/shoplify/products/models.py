from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    unit_price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField()
    cost_price=models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return str(self.name)