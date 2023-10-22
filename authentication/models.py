from django import forms
from captcha.fields import ReCaptchaField
from django.db import models


from createtests.models import StrippedCharField, StrippedTextField


class FormWithCaptcha(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()
