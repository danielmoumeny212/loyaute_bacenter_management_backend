from rest_framework import serializers 
from .models import Service, Bacenter
from django.contrib.auth import get_user_model
from home.models import Profil



User = get_user_model()



    
class ProfilSerializer(serializers.ModelSerializer): 
   class Meta: 
     model = Profil
     fields = ['id', 'statut', 'image']
     

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta: 
        model  = User 
        
class UserSerializer(BaseUserSerializer):
      # profil = ProfilSerializer(many=True)
      
      class Meta(BaseUserSerializer.Meta): 
        fields = ["first_name", "last_name", "email", 'date_joined']

class UserLastFivesLoggedInSerialiser(BaseUserSerializer):
      class Meta(BaseUserSerializer.Meta):
        fields =["first_name", "last_name", "last_login", "email"]

class BacenterPerSerializer(serializers.ModelSerializer):
    newcomer_count = serializers.IntegerField()
    
    class Meta:
        model = Bacenter
        fields = ['name', 'newcomer_count']      

class ChurchStatsSerializer(serializers.Serializer):
    bacenter_count = serializers.IntegerField(default=0)
    bacenter_leader_count = serializers.IntegerField(default=0)
    bacenters_services_count = serializers.IntegerField(default=0)
    services_to_reach = serializers.IntegerField(default=0)
    last_five_users = UserSerializer(many=True)
    last_five_logged_in = UserLastFivesLoggedInSerialiser(many=True)
    newcomers_per_bacenter = BacenterPerSerializer(many=True)
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['last_five_users'] = sorted(
            representation['last_five_users'],
            key=lambda x: x['date_joined'],
            reverse=True
        )[:5]
        return representation

class BaseBacenterSerializer(serializers.ModelSerializer):
  class Meta: 
    model  = Bacenter
    fields = ['id', 'quarter']
    
class BacenterTwoSerializer(BaseBacenterSerializer):
  class Meta(BaseBacenterSerializer.Meta): 
    fields = ['id', 'name', 'quarter']


class ServiceSerializer(serializers.ModelSerializer):
     bacenter = BaseBacenterSerializer(read_only=True)
    #  bacenter_id = serializers.PrimaryKeyRelatedField()
     class Meta: 
       model =  Service
       fields = '__all__'

class CreateServiceSerializer(serializers.ModelSerializer):
      class Meta: 
       model =  Service
       fields = '__all__'

class ServiceStatsSerializer(serializers.Serializer):
    total_new_comer = serializers.IntegerField()
    total_new_convert = serializers.IntegerField()
    total_services = serializers.IntegerField()




class BacenterLeaderSerializer(serializers.ModelSerializer):
   class Meta: 
     model = User
     fields = ['id', 'first_name', 'last_name']

class BacenterSerializer(serializers.ModelSerializer):
     bacenter_leader = BacenterLeaderSerializer(read_only=True)
     class Meta: 
       model = Bacenter
       fields = ['id', 'name', 'quarter', 'bacenter_leader', "deleted"]
    
      
class BacenterCreateSerializer(serializers.ModelSerializer):
     class Meta: 
       model = Bacenter
       fields = ['name', 'quarter', 'bacenter_leader', 'church' ]
       
class BacenterPutSerializer(serializers.ModelSerializer):
     class Meta: 
       model = Bacenter
       fields = ['name', 'quarter', 'bacenter_leader', 'deleted']
      
     
       