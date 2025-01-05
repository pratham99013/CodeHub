from django.forms import ModelForm
from .models import Project, Review
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description' , 'featured_image',  'demo_link', 'source_link', 'tags']
        widgets = {
            'tags' : forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name ,field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'}) 



class ReveiwForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value' , 'body']

    labels = {
        'value' : 'Place your words',
        'body' : 'Add your comment with vote'
    }

    def __init__(self, *args, **kwargs):
        super(ReveiwForm, self).__init__(*args, **kwargs)

        for name ,field in self.fields.items():
            field.widget.attrs.update({'class' : 'input'}) 