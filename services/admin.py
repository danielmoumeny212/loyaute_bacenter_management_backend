from django.contrib import admin
from .models import Service , Bacenter

# Register your models here.

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin): 
    #  fields = '__all__'
    pass 


@admin.register(Bacenter)
class BacenterAdmin(admin.ModelAdmin):
    #  fields = '__all__'
    pass 