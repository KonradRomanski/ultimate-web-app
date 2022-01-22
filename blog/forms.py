from django import forms
from django.contrib.auth.forms import UserCreationForm


# Create your forms here.
from django.contrib.auth.models import User

from blog.models import Comment


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = User

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('description',)
