from django.urls import path 
from . import views 


urlpatterns = [
    path('create', views.profil_detail),
    path('detail/<int:id>', views.profil_detail),
    path('password/reset/confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),    
]
