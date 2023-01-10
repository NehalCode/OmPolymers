
from django.db import models

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50,default="")
    email = models.EmailField()
    password = models. CharField(max_length=50)
    mobile_no = models.BigIntegerField()
    status = models.CharField(max_length=30,default="In-Active")

    def __str__(self):
        return self.email 

    

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField(max_length=500)

class Product_category(models.Model):
    cat_name = models.CharField(max_length=100)
    cat_img = models.ImageField(upload_to='category/', default="default.jpg")

    def __str__(self):
        return self.cat_name

class Product(models.Model):
    product_category = models.ForeignKey(Product_category,on_delete=models.CASCADE)
    Product_name = models. CharField(max_length=100)
    Product_brandname = models.CharField(max_length=500)
    Product_discription = models.TextField(max_length=500)
    Product_price = models.FloatField()
    Product_image = models.ImageField(upload_to='products/', default="default.jpg")
    Product_qty = models.IntegerField()

    def __str__(self):
        return self.Product_name 


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty = models.IntegerField()
    total_price = models.IntegerField()
    dateTime =models.DateTimeField()

    def __str__(self):
        return self.user.firstname + "  |  " + self.product_id.Product_name

        
class Wishlist (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateField()



