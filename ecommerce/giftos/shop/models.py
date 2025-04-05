from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from ckeditor.fields import RichTextField

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
# Product Model
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.CharField(max_length=1500)

    def __str__(self):
        return self.name
# User Model
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class user(AbstractUser):
    username = models.CharField(max_length=100,null=True,blank=True)
    name = models.CharField(max_length=100, unique=True)    
    email = models.EmailField(verbose_name='email', max_length=255, unique=True, null=True)
    phone = models.CharField(max_length=10,blank=True,null=True)
    address = models.CharField(max_length=250,blank=True,null=True)
    password = models.CharField(max_length=100)
    password1 = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]  

    objects = UserManager()

    def __str__(self): 
        return self.name
    
# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    message = models.TextField()

    def __str__(self):
        return self.name

# Slider Model
class Slider(models.Model):
    name = models.CharField(max_length=200)
    image = RichTextField()

    def __str__(self):
        return self.name

# Cart Model
class Cart(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,through='CartItem')
    def __str__(self):
        return self.user.name

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# --------OrderDetails--------

class Order(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    locality = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    address = models.TextField()
    amount = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=300,null=True,blank=True)
    paid = models.BooleanField(default=False,null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way','On the Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),

)
class OrderDetails(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.CharField(max_length=250)
    image = models.ImageField(upload_to="static/images",null=True,blank=True)
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=100)
    total = models.CharField(max_length=100)
    status = models.CharField(max_length=50,default="Pending",choices=STATUS_CHOICE)

    def __str__(self):
        return self.order.user.name
