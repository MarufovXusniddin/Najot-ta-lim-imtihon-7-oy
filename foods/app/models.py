from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nomi')
    slug = models.SlugField(verbose_name='Slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nomi')
    image = models.ImageField(upload_to='prducts/')
    description = models.TextField(verbose_name='Izoh')
    price = models.IntegerField(verbose_name='Narxi')
    quantity = models.IntegerField(default=1000, null=True)
    discount = models.BooleanField(null=True)
    discount_procent = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoriyasi')
    slug = models.SlugField(verbose_name='Slug')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'


class Comment(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Komment mualifi:{self.autor}\n Komment: {self.text}"


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    @property
    def get_cart_total_cart(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price
    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = len(order_products)
        return total_quantity


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    @property
    def get_total_price(self):
        total_price = self.quantity * self.product.price
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(OrderProduct, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, models.SET_NULL, null=True)
    mobile = models.CharField(max_length=13)
    email = models.EmailField(max_length=80)
