from django.db import models

# Create your models here. ok

class Category(models.Model):
    class Meta:
        verbose_name="catagorie"
    category_id=models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=30)
    def __str__(self):
        return f"{self.category_id} --> {self.category_name} "
class Product(models.Model):    
    product_id=models.AutoField(primary_key=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    product_name=models.CharField(max_length=50)
    unit_price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField()
    cost_price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to="products/",null=True,blank=True)
    
    def __str__(self):
        return f"{self.product_id} --> {self.product_name} "
class Sales(models.Model):
    pass