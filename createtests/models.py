from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



# Create your models here.

class StrippedCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.strip() if value else ' '


class StrippedTextField(models.TextField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return value.strip() if value else ' '


class StrippedJSONField(models.JSONField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self._strip_json(value)

    def _strip_json(self, data):
        if isinstance(data, dict):
            return {key.strip(): self._strip_json(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._strip_json(item) for item in data]
        elif isinstance(data, str):
            return data.strip()
        return data


class UserTest(models.Model):
    header = StrippedCharField(max_length=266)
    subtitle = StrippedCharField(max_length=266)
    institution = StrippedCharField(max_length=266)
    add_header_info = StrippedTextField(max_length=1500)
    grades = StrippedJSONField(null=True)
    # question_types will be json with multi-choice, multi-selection and open-answer questions
    question_types = StrippedJSONField(null=True)
    questions = StrippedJSONField(null=True)
    footer = StrippedTextField(null=True, max_length=1500)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    notes = StrippedTextField(null=True, max_length=266)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering: ['-date']

    def save(self, *args, **kwargs):
        # If add_header_info is empty or contains only spaces, set it to an empty string
        self.add_header_info = self.add_header_info.strip() or ' '
        super(UserTest, self).save(*args, **kwargs)

class UserFeedback(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    title = StrippedCharField(max_length=266)
    feedback = StrippedTextField(max_length=3000)
    ranking = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)