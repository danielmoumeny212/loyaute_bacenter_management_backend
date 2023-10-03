from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.permissions import IsAdminUser
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status 
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordResetConfirmView
from .models import Profil , User
from .serializers import ProfilSerializer , CUserSerializer , UserSerializer, UserProfilUpdateSerializer, UserCreateSerializer





class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'home/password_reset_confirm.html'  # Remplacez par votre propre template
    success_url = '/password/reset/complete/'

def hello (request): 
   return render(request, 'home/profil.html')


class CustomUserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer
    
    def get_serializer_context(self):
        statut = self.request.data.get('statut', '')
        # Créer le contexte en incluant la valeur
        context = super().get_serializer_context()
        context['statut'] = statut

        return context
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomUserCreateView(CreateAPIView):
#     serializer_class =  UserCreateSerializer
    
#     def get_serializer_context(self):
#         statut = self.request.data.get('statut', '')
#         print(self.request.data)

#         # Créer le contexte en incluant la valeur
#         context = super().get_serializer_context()
#         context['statut'] = statut

#         return context
    
#     def post(self, request, *args, **kwargs):
#         create_serializer = UserCreateSerializer(data=request.data)
#         if create_serializer.is_valid():
#             user = create_serializer.save()
#             serializer = UserSerializer(user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
@user_passes_test(lambda user: user.is_staff)
@login_required
def deactivate_user(request, id):
    user = get_object_or_404(User, pk=id)
    user.is_active = False
    user.save()
    serializer = CUserSerializer(instance=user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@user_passes_test(lambda user: user.is_staff)
@login_required
def activate_user(request, id): 
    user = get_object_or_404(User, pk=id)
    user.is_active = True
    user.save()
    serializer = CUserSerializer(instance=user)
    return Response(serializer.data, status=status.HTTP_200_OK)
 

@api_view(['PUT'])
@user_passes_test(lambda user: user.is_staff)
@login_required
def update_user(request, id):
    try:
        user = User.objects.get(pk=id)
        serializer = UserProfilUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response("User not found", status=status.HTTP_404_NOT_FOUND)

   
   

@api_view(['POST'])
@login_required()
def create_profil(request): 
   if request.method == 'POST':
       request.data['user_id'] = request.user.id 
       serializer = ProfilSerializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       serializer.validated_data 
       serializer.save()
       return Response(serializer.data, status=status.HTTP_201_CREATED)
   return Response({'error': status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT'])
@login_required()
def profil_detail(request, id): 
   profil = get_object_or_404(Profil, pk=id)
   if request.method == 'GET': 
      serializer = ProfilSerializer(instance=profil)
      return Response(serializer.data, status=status.HTTP_200_OK)
   elif request.method == 'PUT': 
      serializer = ProfilSerializer(instance=profil, data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.validated_data 
      serializer.save()
      return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


