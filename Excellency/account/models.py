from django.db import models
from django.contrib.auth.models import AbstractUser

from main import validator


def group_based_upload_to(instance, filename):
   return "profiles/images/{}/{}".format(instance.user.id, filename)


class User(AbstractUser):
   national_id = models.CharField(max_length=10, unique=True, validators=[
                                  validator.validate_national_id])
   email = models.EmailField(max_length=100, unique=True, validators=[
    validator.validate_email])
   full_name = models.CharField(max_length=50)
   USERNAME_FIELD = "email"
   REQUIRED_FIELDS = ['username', 'full_name']

   def __str__(self):
      return self.username


class CustomarProfile(models.Model):

   class gender_choices(models.TextChoices):
      null = ""
      Male = "ذكر"
      Female = "انثى"

   user = models.OneToOneField(User, on_delete=models.CASCADE)
   phone = models.CharField(max_length=10, unique=True, validators=[
                            validator.validate_phone])
   image = models.ImageField(
       upload_to=group_based_upload_to, default="profiles/images/user-defualt.svg")
   gender = models.CharField(max_length=22,
                             choices=gender_choices.choices,
                             default=gender_choices.null)

   def __str__(self) -> str:
      return f"{self.user.username}"
