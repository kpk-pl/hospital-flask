from django.db import models
import datetime

class User(models.Model):
    ADMIN, SALESMAN, USER = 'A', 'S', 'U';
    RIGHTS_CHOICES = (
        (ADMIN, 'Admin'),
        (SALESMAN, 'Salesman'),
        (USER, 'User'),
    )
    
    rights = models.CharField(name="Rights",
        max_length=1,
        choices=RIGHTS_CHOICES,
        default=USER)
    
    first_name = models.CharField(name="First name", max_length=128)
    last_name = models.CharField(name="Last name", max_length=128)
    address = models.CharField(name="Address", max_length=256)
    postal_code = models.CharField(name="Postal code", max_length=16)
    city = models.CharField(name="City", max_length=128)
    phone = models.CharField(name="Phone", max_length=32)
    date_registered = models.DateField(name="Registration date", auto_now_add=True)
    
    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
        
class ProductCategory(models.Model):
    name = models.CharField(name="Category name", 
        max_length=128,
        unique=True)
        
    def __unicode__(self):
        return self.name
     
class Product(models.Model):
    category = models.ForeignKey(ProductCategory)
    description = models.TextField(name="Product description")
    photo = models.CharField(name="Path to photo", max_length=256)
    price = models.DecimalField(name="Price", decimal_places=2, max_digits=10)
    stack = models.PositiveIntegerField(name="Stack")
    
    producent = models.CharField(name="Producent", max_length=256)
    model = models.CharField(name="Model", max_length=512)
    
    def __unicode__(self):
        return self.model + ' ' + self.producent
        
class Order(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(name="Order date", auto_now_add=True)
    id = models.AutoField(primary_key=True)
    
    def __unicode__(self):
        return "Order " + id
       
