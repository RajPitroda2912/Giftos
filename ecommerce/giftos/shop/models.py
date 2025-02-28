from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
# Create your models here.

CATEGORY_CHOICES = (
    ('T', 'Teddy'),
    ('W', 'Watch'),
    ('P', 'Perfume')
)

class Product(models.Model):
    title = models.CharField(max_length=120)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=200)
    status = models.CharField(max_length=200)
    image = models.CharField(max_length=2855)

    def __str__(self):
        return self.title
    

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
	username = None
	name = models.CharField(max_length=100, unique=True)	
	email = models.EmailField(verbose_name='email', max_length=255, unique=True, null=True)
	password = models.CharField(max_length=100, null=True)
	password1 = models.CharField(max_length=100, null=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name',]  

	objects = UserManager()

	def __str__(self): 
		return self.name
    

class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    message = models.TextField()

    def __str__(self):
        return self.name