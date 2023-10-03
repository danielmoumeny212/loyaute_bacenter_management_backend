from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.contrib.auth import views as auth_views
from . import settings
from home.views import deactivate_user , activate_user, update_user, CustomUserCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profil/',  include('home.urls')),
    path('church/', include('services.urls')),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password/reset/confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/users/create', CustomUserCreateView.as_view()),
    path('auth/users/update/<int:id>/', update_user),
    path('auth/users/deactivate/<int:id>/', deactivate_user),
    path('auth/users/activate/<int:id>/', activate_user),
] 
if settings.DEBUG: 
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
