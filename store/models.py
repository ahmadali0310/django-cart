from django.db import models
from django.contrib.auth.models import  User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
        name = models.CharField(max_length=200, null=True)
        price = models.DecimalField(max_digits=20,decimal_places=2)
        digital = models.BooleanField(default=False, null=True, blank=False)
        image = models.ImageField(upload_to='media')

        def __str__(self): 
            return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_items_quantity(self):
        order_items = self.orderitem_set.all()
        quantity = sum([item.quantity for item in order_items])
        return quantity
    
    @property
    def get_items_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_product_total for item in order_items])
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True) 

    @property
    def get_product_total(self):
        total = self.quantity * self.product.price
        return total


