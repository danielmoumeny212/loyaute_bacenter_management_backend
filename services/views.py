from django.db.models import Sum , Count , Value
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required , user_passes_test
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound

from rest_framework.response import Response 
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView , CreateAPIView
from rest_framework.decorators import api_view 

from .serialisers import (ServiceSerializer, ServiceStatsSerializer, BacenterSerializer, BacenterCreateSerializer , BacenterPutSerializer, ChurchStatsSerializer, CreateServiceSerializer)
from .models import Service, Bacenter, Church
from home.serializers import UserSerializer



User = get_user_model()

# Create your views here.

class ChurchUserView(ListAPIView): 
    serializer_class  = UserSerializer
    
    def  get_queryset(self):
        church_id = self.kwargs.get('church_id')
        queryset = User.objects.filter(church_id=church_id).order_by('last_name')
        return queryset 




class ChurchRequestMixin: 
    
    def get_last_five_recently_logged_in_users(self, church_id):
        users = User.objects.filter(church_id=church_id).exclude(last_login=None).order_by('-last_login')[:5]
        return users if users.exists() else []
    
    def get_last_five_users(self, church_id):
        users = User.objects.filter(church_id=church_id).order_by('-date_joined')[:5]
        return users if users.exists() else []
    
    def bacenter_count(self, church_id):
        return  Bacenter.objects.filter(church_id=church_id).count()
    
    def users_count(self, church_id):
        return User.objects.filter(church_id=church_id).count()
    
    def get_newcomers_per_bacenter(self, church_id):
        newcomers_per_bacenter = Bacenter.objects.filter(church_id=church_id) \
            .annotate(newcomer_count=Coalesce(Sum('service__new_comer'), Value(0))) \
            .order_by('newcomer_count')
        return newcomers_per_bacenter
    
    def bacenters_services_count(self,church_id):
        total_services_count = Service.objects.filter(bacenter__church_id=church_id).count()
        return total_services_count
      
     
    

class ChurchStatsView(ChurchRequestMixin,APIView):
    
    def calculate_total_meetings_per_year(self,meetings_per_week):
        weeks_per_year = 52
        total_meetings = meetings_per_week * weeks_per_year
        return total_meetings

    
    
    def get(self, request, church_id, *args, **kwargs):
        if not Church.objects.filter(id=church_id).exists():
            raise NotFound("Church not found")

        bacenter_leader_count =self.users_count(church_id)
        bacenter_count = self.bacenter_count(church_id)
        last_five_users = self.get_last_five_users(church_id)
        last_five_logged_in = self.get_last_five_recently_logged_in_users(church_id)
        bacenters_services_count = self.bacenters_services_count(church_id)
        services_to_reach = self.calculate_total_meetings_per_year(1) * bacenter_count
        newcomers_per_bacenter = self.get_newcomers_per_bacenter(church_id)

        data = {
            "bacenter_leader_count": bacenter_leader_count,
            "bacenter_count": bacenter_count,
            "bacenters_services_count":  bacenters_services_count,
            "services_to_reach": services_to_reach,
            "last_five_users": last_five_users.values(),
            "last_five_logged_in": last_five_logged_in.values(),
            "newcomers_per_bacenter": newcomers_per_bacenter.values(),
        }
        serializer = ChurchStatsSerializer(instance=data)  
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    
class BacenterListView(ListAPIView):
    serializer_class = BacenterSerializer
    
    def get_queryset(self):
        church_id = self.kwargs['church_id']
        queryset = Bacenter.objects.filter(church_id=church_id, deleted=False)
        return queryset
        
    


class BacenterCreateView(CreateAPIView):
    serializer_class = BacenterCreateSerializer

    def post(self, request, *args, **kwargs):
        create_serializer = BacenterCreateSerializer(data=request.data)
        if create_serializer.is_valid():
            bacenter = create_serializer.save()
            serializer = BacenterSerializer(bacenter)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
        
        
class BacenterRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Bacenter.objects.all()
    serializer_class = BacenterSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()  # Récupérer l'instance existante
        put_serializer = BacenterPutSerializer(instance, data=request.data)
        put_serializer.is_valid(raise_exception=True)
        put_serializer.save()  # Mettre à jour l'instance existante
        serializer = BacenterSerializer(instance)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

       

class ServiceListCreateView(ListCreateAPIView): 
     lookup_field =  'bacenter_id' 
     
     def get_serializer_class(self):
           if self.request.method == 'POST':
                return CreateServiceSerializer
           return ServiceSerializer
       
     def get_queryset(self):
        bacenter_id = self.kwargs['bacenter_id']
        queryset = Service.objects.filter(bacenter_id=bacenter_id)
        
        return queryset
    
class ServiceRetrieveUpdateView(RetrieveUpdateAPIView): 
       serializer_class = ServiceSerializer
       lookup_field =  'bacenter_id'
       
       
       def get_queryset(self):
          bacenter_id = self.kwargs['bacenter_id']
          service_id = self.kwargs['service_id']
          queryset = Service.objects.filter(bacenter_id=bacenter_id, pk=service_id)
          return queryset
       
class ServiceStatsView(APIView):
    
    
    def get(self, request, church_id ,bacenter_id):
        services = Service.objects.filter(bacenter_id=bacenter_id)
       
        service_stats = services.aggregate(
            total_new_comer=Coalesce(Sum('new_comer'), 0),
            total_new_convert=Coalesce(Sum('new_convert'), 0),
            total_services=Count('id')
        )
        serializer = ServiceStatsSerializer(service_stats)
        return Response(serializer.data)








@api_view(['PUT'])
@login_required()
@user_passes_test(lambda u: u.is_admin)
def remove_bacenter(request):
  if request.method == 'PUT':
    request.data['bacenter_leader'] = request.user.id
    serializer = ServiceSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.validated_data 
    serializer.save()
    return Response(serializer.data , status=status.HTTP_200_OK)
  


# class BacenterCreateView(CreateAPIView): 
#       serializer_class = BacenterCreateSerializer
      
#       def post(self, request, *args, **kwargs):
#         create_serializer = BacenterCreateSerializer(data=request.data)
#         if create_serializer.is_valid():
#             bacenter = create_serializer.update(request.data)
#             serializer = BacenterSerializer(bacenter)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
