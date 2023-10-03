from django.db import models
from django.conf import settings 
from home.models import Church
# Create your models here.

class Bacenter(models.Model):
  name = models.CharField(max_length=255)
  quarter = models.CharField(max_length=255)
  bacenter_leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
  church = models.ForeignKey(Church, on_delete=models.PROTECT)
  deleted = models.BooleanField(default=False)
  
  
  def __str__(self):
      return self.name
  
class AbstractEntity(models.Model):
  name = models.CharField(max_length=255)
  preacher = models.CharField(max_length=200)
  attendance = models.PositiveSmallIntegerField(default=0)
  new_comer = models.PositiveSmallIntegerField(default=0)
  new_convert = models.PositiveSmallIntegerField(default=0)
  offrandes = models.PositiveBigIntegerField(default=0)
  tithes = models.PositiveBigIntegerField(default=0)
  date = models.DateField(auto_now_add=True)
  
  class Meta:
        abstract = True
  
  def __str__(self):
    return self.name 
    

class Cultes(AbstractEntity):
      pass 
  
    
class Service(models.Model):
  service_name = models.CharField(max_length=255)
  predicator = models.CharField(max_length=200)
  attendance = models.PositiveSmallIntegerField(default=0)
  new_comer = models.PositiveSmallIntegerField(default=0)
  new_convert = models.PositiveSmallIntegerField(default=0)
  offrandes = models.PositiveBigIntegerField(default=0)
  tithes = models.PositiveBigIntegerField(default=0)
  bacenter = models.ForeignKey(Bacenter, on_delete=models.PROTECT)
  date = models.DateField(auto_now_add=True)
  photo = models.ImageField(upload_to='services', blank=True, null=True)
  
  
  def __str__(self):
     return self.service_name 

  