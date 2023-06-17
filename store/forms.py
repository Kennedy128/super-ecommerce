from django import forms
from .models import Profile,Project,Review

    
class ProfileForm(forms.ModelForm):
    '''
    class to define profile form
    '''
    class Meta:
        model = Profile
        exlcude = ['user']
        fields = ('bio', 'profile_pic')


class ProjectForm(forms.ModelForm):
    '''
    class to define project form
    '''
    class Meta:
        model = Project
        exlcude = ['user']
        fields = ('title','description','image') 

class ReviewForm(forms.ModelForm):
    '''
    class to define Review form
    '''
    class Meta:
        model = Review
        exlcude = ['user','project']
        fields = ('comment','availability','ratings')