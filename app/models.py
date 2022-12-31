import pathlib
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

STATE_CHOICES = (
    ('Andaman & Nicobar Island', 'Andaman & Nicobar Island'),
    ('karachi', 'karachi'),
    ('islamabad', 'islamabad'),
    ('karachi', 'karachi'),
    ('peshawar', 'peshawar'),
    ('lahore', 'lahore'),
    ('sargodha', 'sargodha'),
    ('jhang', 'jhang'),
    ('rawalpindi', 'rawalpindi'),
    ('d.i khan', 'd.i khan'),
    ('banu', 'banu'),
    ('haiderabad', 'haiderabad'),
    ('sakhar', 'sakhar'),
    ('rohri', 'rohri'),
    ('DG Khan', 'DG Khan'),
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=5)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return str(self.id)


CATEGORY_CHOICES = (
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('B', 'Bottom Wear'),
)

# function for generating unique name images for "Product"


# def ProductImageUploadHandler(instance, filename):
#     file_path = pathlib.Path(filename)
#     new_img_name = str(uuid.uuid1())  # uuid1 -> uuid + timestamps
#     # file_path.suffix: abc.png def.img
#     return f"productimg/{new_img_name}{file_path.suffix}"


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    descounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    # rather then saving image with original name, make a unique name by uui+time stamp,
    product_image = models.FileField(upload_to='productimg/')
    # product_image = models.ImageField(upload_to="productimg/")

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)


# to get the cost of single product from the cart acc to quantity of that product in cart..now we can pass this total_cost to our checkout template to get the cost of a single product acc to its quantity


    @property
    def total_cost(self):
        return self.quantity * self.product.descounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Deliverd', 'Deliverd'),
    ('Cancel', 'Cancel'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.descounted_price
