from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skills, Message



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class Profileform(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email' , 'username', 'location', 'short_intro', 'bio', 'profile_image', 'social_github', 'social_linkedin']

    
    def __init__(self, *args, **kwargs):
        super(Profileform, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})




class SkillForm(ModelForm):
    class Meta:
        model = Skills
        fields = ['name' , 'description']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})



class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body'] 

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})