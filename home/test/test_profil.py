import pytest 
from model_bakery import baker 

from home.models import Profil, User
from rest_framework import status 


@pytest.fixture
def create_profil(api_client):
  def do_create_profil(profil): 
    return api_client.post('profil/create',data=profil, content_type='application/json')
  return do_create_profil


# @pytest.mark.django_db
# class TestCreateProfil: 
  
#     def test_if_anonymous_user_can_create_profil_returns_403(self, create_profil): 
#       user = baker.make(User, id=14)
#       # print(user.__dict__)
#       profil = baker.make(Profil, user=user, id=12)
#       print(profil.__dict__)
      
#       response = create_profil(profil)
      
#       response.status_code == status.HTTP_403_FORBIDDEN