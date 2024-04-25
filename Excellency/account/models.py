from django.db import models
from django.contrib.auth.models import AbstractUser
from service.models import Specialty

from main import validator


def group_based_upload_to(instance, filename):
   return "profiles/images/{}/{}".format(instance.user.id, filename)


class User(AbstractUser):
   SUPERVISOR = "ادارة"
   Lawyer = "محامي"
   Customar = "عميل"
   ROLE_CHOICES = (
       ('Supervisor', SUPERVISOR),
       ('Lawyer', Lawyer),
       ('Customar', Customar),
    )
   national_id = models.CharField(max_length=10, unique=True, validators=[
                                  validator.validate_national_id])
   email = models.EmailField(max_length=100, unique=True, validators=[
    validator.validate_email])
   full_name = models.CharField(max_length=50, blank=False)
   role = models.CharField(max_length=15,
                           choices=ROLE_CHOICES, null=True, blank=True)
   USERNAME_FIELD = "email"
   REQUIRED_FIELDS = ['username', 'full_name']

   def __str__(self):
      return self.username


class gender_choices(models.TextChoices):
   Male = "ذكر"
   Female = "انثى"


class CustomarProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   phone = models.CharField(max_length=10, unique=True, validators=[
                            validator.validate_phone])
   image = models.ImageField(
       upload_to=group_based_upload_to, default="profiles/images/user-defualt.svg")
   gender = models.CharField(max_length=22,
                             choices=gender_choices.choices,
                             null=True, blank=True)

   def __str__(self) -> str:
      return f"{self.user.full_name}"


class LawyerProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   phone = models.CharField(max_length=10, unique=True, validators=[
       validator.validate_phone])
   image = models.ImageField(
      upload_to=group_based_upload_to, blank=False)
   gender = models.CharField(max_length=22,
                             choices=gender_choices.choices,
                             null=True, blank=True)
   specialty = models.ManyToManyField(Specialty)
   certified = models.BooleanField(default=False)
   licence = models.FileField(blank=False)
   Qualification = models.FileField(blank=False)

   def __str__(self) -> str:
      return f"{self.user.full_name}"
