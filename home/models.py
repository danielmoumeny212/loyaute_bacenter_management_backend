from django.db import  models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.$

class Church (models.Model):
    name = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.name
    
    
    class Meta: 
      verbose_name_plural = "Churches"
    
class CustomUserManager(BaseUserManager):
  
    def _create_user(self, email, password,  **other_fields):
      if not email: 
        raise ValueError("Email Should not be empty")
      if not password: 
          raise ValueError("Password Should not be empty")
      user = self.model(
        email = self.normalize_email(email),
        **other_fields
      )
      user.set_password(password)
      user.save(using=self._db)
      return user 
    
    def create_user(self, email, password, **other_fields):
      other_fields.setdefault('is_staff', False)
      other_fields.setdefault('is_superuser', False)
      other_fields.setdefault('is_active', True)
      return self._create_user(email, password, **other_fields)
    
    def create_superuser(self, email, password, **other_fields):
      other_fields.setdefault('is_staff', True)
      other_fields.setdefault('is_superuser', True)
      other_fields.setdefault('is_active', True)
      return self._create_user(email, password, **other_fields)
       

class User(AbstractBaseUser, PermissionsMixin):
      email = models.EmailField(unique=True, max_length=254 , db_index=True)
      first_name = models.CharField(max_length=240, blank=True)
      last_name = models.CharField(max_length= 255, blank=True)
      date_joined =  models.DateField(default=timezone.now)
      is_staff = models.BooleanField(default=False)
      is_active = models.BooleanField(default=True)
      is_superuser = models.BooleanField(default=False)
      church = models.ForeignKey(Church, on_delete=models.PROTECT)
      
      objects = CustomUserManager()
      USERNAME_FIELD = 'email'
      REQUIRED_FIELDS = []
      
   
      class Meta: 
       verbose_name = "User"
       verbose_name_plural = 'users'
      
      def __str__(self): 
        return f"{self.first_name} {self.last_name}"




class Profil(models.Model): 
    STATUT_CHOICE =  [
    ('Pasteur', 'Pasteur'),
    ('Berger', 'Berger'),
    ('Potentiel Berger', 'Potentiel Berger'),
    ('Ms', 'Ms'),]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    image = models.ImageField(upload_to='userPic', blank=True, null=True)
    cellphone_number = models.CharField(max_length=18, default="", blank=True)
     
    def __str__(self):
      return f"{self.user.email} | {self.statut}"