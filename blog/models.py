from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from djongo import models

class Post(models.Model):
    title = models.CharField(max_length=450)
    author_id = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title


class NeuralNetworkData(models.Model):
    date = models.CharField(max_length=30)
    price = models.FloatField()
    bedrooms = models.IntegerField()
    bathrooms = models.FloatField()
    sqft_living = models.IntegerField()
    sqft_lot = models.IntegerField()
    floors = models.IntegerField()
    waterfront = models.IntegerField()
    view = models.IntegerField()
    condition = models.IntegerField()
    sqft_above = models.IntegerField()
    sqft_basement = models.IntegerField()
    yr_built = models.IntegerField()
    yr_renovated = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    statezip = models.CharField(max_length=30)
    country = models.CharField(max_length=50)


class ModelMetrics(models.Model):
    mae = models.FloatField()
    mse = models.FloatField()
    rmse = models.FloatField()

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="blog_user_set",  # Unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="blog_user_permission_set",  # Unique related_name
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
