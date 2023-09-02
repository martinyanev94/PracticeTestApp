from django import forms
from captcha.fields import ReCaptchaField

class FormWithCaptcha(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField()
