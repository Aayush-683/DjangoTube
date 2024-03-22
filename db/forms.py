from django import forms
from .models import Videos

attrs = {
    "type": "password"
}
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True, widget=forms.TextInput(attrs=attrs))

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True, widget=forms.TextInput(attrs=attrs))
    confirm_password = forms.CharField(label='Confirm Password', max_length=100, required=True, widget=forms.TextInput(attrs=attrs))

class VideoForm(forms.ModelForm):
    class Meta:
        model = Videos
        fields = ['title', 'video', 'thumbnail', 'description']
        labels = {
            'title': 'Title',
            'video': 'Video',
            'thumbnail': 'Thumbnail Image',
            'description': 'Video Description'
        }
    
    def __init__(self, *args, **kwargs):
        super(VideoForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['video'].required = True
        self.fields['thumbnail'].required = True
        self.fields['description'].required = True