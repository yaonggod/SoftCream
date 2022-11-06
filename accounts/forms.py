from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import Profile


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            "username",
            "password1",
            "password2",
            "last_name",
            "email",
        )
        labels = {
            "username": "아이디",
            "password1": "비밀번호",
            "password2": "비밀번호 확인",
            "last_name": "이름",
            "email": "이메일",
        }


class UpdateForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
        )
        labels = {
            "email": "이메일",
            "first_name": "성",
            "last_name": "이름",
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "image",
            "status",
        ]
        labels = {"image": "프로필 이미지", "status": "상태 메세지"}
