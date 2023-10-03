from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer 
from djoser.serializers import UserSerializer as BaseUserSerializer 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers
from .models import Profil , Church
from services.serialisers import BacenterTwoSerializer




from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profil, Church



from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profil, Church


class UserCreateSerializer(BaseUserCreateSerializer):
    email = serializers.EmailField(required=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['password', 'first_name', 'last_name', 'is_staff', 'email', 'id', 'church']

    def create(self, validated_data):
        user = super().create(validated_data)  # Crée l'utilisateur de base

        profil = user.profil
        statut = self.context.get('statut')
    
        if statut is not None:
            profil.statut = statut
            profil.save()

        return user


    
class ProfilSerializer(serializers.ModelSerializer): 
   class Meta: 
     model = Profil
     fields = ['id', 'statut', 'image', 'cellphone_number']
     


class ChurchSerializer(serializers.ModelSerializer):
    class Meta: 
       model = Church
       fields = ['id', 'name']

class CurrentUserSerializer(BaseUserSerializer):
     class Meta(BaseUserSerializer.Meta): 
        fields = ['id', 'first_name', 'last_name', 'email','is_staff']

class UserUpdateSerializer(BaseUserSerializer):
   class Meta(BaseUserSerializer.Meta): 
        fields = [ 'first_name', 'last_name', 'email','is_staff']
   
class UserSerializer(BaseUserSerializer):
   profil = ProfilSerializer()
   bacenters= BacenterTwoSerializer(many=True, read_only=True, source="bacenter_set")
   church =  ChurchSerializer()
   
   class Meta(BaseUserSerializer.Meta):
      fields = ['id', 'first_name', 'last_name', 'email', 'is_staff', 'last_login', 'profil', 'is_active', 'bacenters', 'church']
      
class CUserSerializer(serializers.ModelSerializer):
   profil = ProfilSerializer()
   class Meta(BaseUserSerializer.Meta):
      fields = ['id', 'first_name', 'last_name', 'email', 'is_staff', 'last_login', 'profil', 'is_active']

class UserProfilUpdateSerializer(serializers.Serializer):
   #  username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    is_staff = serializers.BooleanField(required=False)
    statut = serializers.CharField(required=False)

    def update(self, user, validated_data):
        # Mettre à jour les champs du modèle User
        for attr, value in validated_data.items():
            setattr(user, attr, value)
        user.save()

        # Mettre à jour le champ 'statut' dans le modèle Profil
        profil = user.profil
        statut = validated_data.get('statut')
        if statut is not None:
            profil.statut = statut
            profil.save()

        return user



class MyTokenObtainPairSerializer(TokenObtainPairSerializer): 
    
    @classmethod
    def get_token(cls, user): 
       token = super().get_token(user)
       token['is_admin'] = user.is_staff 
       return token 
       