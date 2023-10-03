from django.urls import  path 
from . import views

urlpatterns = [
    path('<int:church_id>/stats', views.ChurchStatsView.as_view()),
    path('<int:church_id>/users', views.ChurchUserView.as_view()),
    path('<int:church_id>/bacenters', views.BacenterListView.as_view()),
    path('<int:church_id>/bacenters/create', views.BacenterCreateView.as_view()),
    path('<int:church_id>/bacenters/<int:pk>', views.BacenterRetrieveUpdateView.as_view()),
    path('<int:church_id>/bacenters/<int:bacenter_id>/stats', views.ServiceStatsView.as_view()),
    path('<int:church_id>/bacenters/<int:bacenter_id>/services', views.ServiceListCreateView.as_view()),
    path('<int:church_id>/bacenters/<int:bacenter_id>/services/<int:service_id>', views.ServiceRetrieveUpdateView.as_view()),
    # path('all/user/<int:id>', views.get_service_list_user),
    # path('detail/<int:id>', views.service_detail), 
    # path('login/', views.login)
]
