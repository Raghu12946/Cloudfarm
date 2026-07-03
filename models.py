from django.db import models
from django.core.validators import RegexValidator


# Model for Registration
class UserRegistration(models.Model):
    number = models.CharField(
        max_length=10,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits.",
                code='invalid_phone_number'
            )
        ],
    )
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name



# Model for Login
from django.contrib.auth.models import AbstractUser
class UserLogin(models.Model):
    number = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, to_field='number')
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"Login attempt by: {self.number}"
    
class Fertilizer(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    suitable_crops = models.TextField(help_text="Comma-separated list of suitable crops")
    image = models.ImageField(upload_to='fertilizer_images/')

    def __str__(self):
        return self.name

