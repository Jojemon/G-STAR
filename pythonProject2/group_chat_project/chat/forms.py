from django import forms
from .models import Room, Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'section']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    SECTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('S', 'S'),
        ('', 'None')

    ]
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    section = forms.ChoiceField(choices=SECTION_CHOICES, required=False)  # Optional for teachers

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'section')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        section = cleaned_data.get('section')

        if role == 'student' and not section:
            raise forms.ValidationError("Students must select a section.")
        return cleaned_data