from django import forms
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm as BaseSignupForm

CustomUser = get_user_model()

class CustomSignupForm(BaseSignupForm):
    first_name = forms.CharField(max_length=30, label='Prénom')
    last_name = forms.CharField(max_length=30, label='Nom')
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'profile_picture', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        } 