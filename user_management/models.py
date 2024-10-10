from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    
    class CustomUserGender(models.IntegerChoices):
        male = (1,'Male')
        female = (2,'Female')
        other = (3,'Other')
        __empty__ = ('-- Gender --')
        
    phone_number = models.CharField(verbose_name='Phone number', max_length=50)
    gender = models.IntegerField(verbose_name='Gender',choices=CustomUserGender)
    
    def __str__(self):
        return self.username
    
    