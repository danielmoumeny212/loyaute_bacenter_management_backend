from django.contrib import admin
from .models import User , Profil, Church

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin): 
     pass 
   
@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
     pass 

@admin.register(Church)
class ChurchAdmin(admin.ModelAdmin):
     pass 
