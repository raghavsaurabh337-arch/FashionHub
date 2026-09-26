from django.db import models

class Register(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name    
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('kids', 'Kids'),
    ('accessories', 'Accessories'),
]
SIZE_CHOICES = [
    ('M', 'M'),
    ('L', 'L'),
    ('X', 'X'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
   
]

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=15,
        choices=GENDER_CHOICES
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    size = models.CharField(
            max_length=4,
            choices=SIZE_CHOICES
        )
    color = models.CharField(max_length=50, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name