from django.contrib.auth.models import User
from rest_framework import status 
from model_bakery import baker
import pytest

from services.models import Service


@pytest.fixture
def create_service(api_client):
   def do_create_service(service):
      return api_client.post('/service/create', data=service, content_type='application/json')
   return do_create_service



@pytest.mark.django_db
class TestGetServices: 
   
   def test_if_user_is_not_admin_get_services_returns_405(self, authenticate, api_client):
      authenticate()

      response = api_client.get('/service/all')
      
      assert response.status_code == status.HTTP_302_FOUND
      
   def test_if_user_is_admin_get_services_returns_200(self, authenticate, api_client):
      authenticate(is_staff=True)
      response = api_client.get('/service/all')
      
      assert response.status_code == status.HTTP_200_OK
      

@pytest.mark.django_db
class TestCreateService:
    
    def test_if_user_anonymous_redirected_returns_302(self, create_service):
       #Arrange 
       #Act 
       response = create_service({})
       #Assert 
       assert response.status_code == status.HTTP_302_FOUND
         
    def test_if_user_authenticated_not_valid_data_submit_returns_400(self, authenticate, create_service):
       authenticate(is_staff=False)
       response = create_service({'title': 'a'})
       assert response.status_code == status.HTTP_400_BAD_REQUEST
       
         
   #  def test_if_user_authenticated_valid_data_submitted_return_201(self, authenticate, create_service):
   #       authenticate(is_staff=False)
   #       response = create_service(baker.make(Service))
         
         
   #       assert response.status_code == status.HTTP_201_CREATED
         


# @pytest.mark.django_db
# class TestRetrieveService: 
#    def test_if_service_exists_returns_200(self,api_client):
#         service = baker.make(Service)
        
#         response = api_client.get(f'/service/detail/2/')
        
       
#         assert response.status_code == status.HTTP_200_OK
     
        