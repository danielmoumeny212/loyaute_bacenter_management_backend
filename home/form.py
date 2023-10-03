from django import forms
from .models import User, Profil


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'class': 'form-control top mb-4',
            'placeholder': "nom d'utilisateur",

        }
    ))
    password = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={
            'class': 'form-control bottom',
            'placeholder': 'mot de passe',
            'type': 'password',
        }
    ))


class UserCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
           self.fields[key].widget.attrs = {
            'class': "form-control", "style": "font-size: 1.6rem;", "required":""}
             

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        
        
class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for key in self.fields.keys():
           self.fields[key].widget.attrs = {
            'class': "form-control", 
            "style": "font-size: 1.6rem;", 
            }
    
    new_password = forms.CharField(max_length=255 , required=False)
    old_password = forms.CharField(max_length=255 , required=False)
             

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserProfilCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
      super(UserProfilCreationForm, self).__init__(*args, **kwargs)
      self.fields['statut'].widget.attrs = {
        'class': 'form-select', 
        'type': 'select',
        'style': 'font-size: 1.6rem;'
      }
      self.fields['is_admin'].widget.attrs = {
        'class': 'form-check-input me-2 ', 
        'style': 'font-size: 1.6rem;'
      }
    
    class Meta: 
        model = Profil 
        fields = ['statut', 'is_admin']
        

class UserUpdateProfilForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
      super(UserUpdateProfilForm, self).__init__(*args, **kwargs)
      self.fields['statut'].widget.attrs = {
        'class': 'form-select', 
        # 'type': 'select',
        'style': 'font-size: 1.6rem;'
      }
      self.fields['is_admin'].widget.attrs = {
        'class': 'form-check-input me-2 ', 
        'style': 'font-size: 1.6rem;'
      }
      self.fields['image'].widget.attrs = {
          'class': "form-control",
         'style': 'font-size: 1.6rem;'
           
      }
    
    class Meta: 
        model = Profil 
        exclude = ['user']