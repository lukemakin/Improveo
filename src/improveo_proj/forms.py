from django import forms
from django.utils.safestring import mark_safe

class CustomSignupForm(forms.Form):

    check = forms.BooleanField(
        required=True, label_suffix='', label=mark_safe("I accept terms of <a href=http://somerandomlinkwithpricvacypolicy.com/privacy_policy class='text-blue-400 hover:text-blue-800'> privacy policy </a>"))

    field_order = ['username', 'email', 'password1', 'password2', 'check']
    
    def signup(self, request, user):
        user.check = self.cleaned_data['check']
        user.save()
        return user

  
