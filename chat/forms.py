from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Type a message. Use @ to tag users...',
        'autocomplete': 'off',
        'id': 'message-input'
    }))

    class Meta:
        model = Message
        fields = ['content']
