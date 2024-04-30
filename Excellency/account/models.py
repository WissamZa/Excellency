from django.db import models
from django.contrib.auth.models import AbstractUser

from main import validator


def images_upload_to(instance, filename):
   return "profiles/{}/images/{}".format(instance.user.id, filename)


def licences_upload_to(instance, filename):
   return "profiles/{}/licence/{}".format(instance.user.id, filename)


def qualification_upload_to(instance, filename):
   return "profiles/{}/qualification/{}".format(instance.user.id, filename)


legal_advice = "استشارات قانونية"
drafting_contracts = "صياغة عقود"
warrant = "مذكرات"

Specialty_CHOICES = {
    'legal_advice': legal_advice,
    'drafting_contracts': drafting_contracts,
    'warrant': warrant
}


class Specialty(models.Model):
   name = models.CharField(max_length=20, unique=True)

   def __str__(self):
      return self.name


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
   # bannar = models.ImageField(
   #    upload_to=group_based_upload_to, default="profiles/images/gold-icon.png")
   USERNAME_FIELD = "email"
   REQUIRED_FIELDS = ['username', 'full_name', 'role']

   def __str__(self):
      return self.username


class gender_choices(models.TextChoices):
   Male = "ذكر"
   Female = "انثى"


class CustomarProfile(models.Model):
   user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name="customar_profile")
   phone = models.CharField(max_length=10, blank=True, validators=[
                            validator.validate_phone])
   image = models.ImageField(
       upload_to=images_upload_to, default="/profiles/images/user-default.png")
   bannar = models.ImageField(
       upload_to=images_upload_to, default="/profiles/images/banner.jpg")
   gender = models.CharField(max_length=22,choices=gender_choices.choices,null=True, blank=True)

   def __str__(self) -> str:
      return f"{self.user.full_name}"


class LawyerProfile(models.Model):
   user = models.OneToOneField(
      User, on_delete=models.CASCADE, related_name="lawyer_profile")
   phone = models.CharField(max_length=10, unique=True, validators=[
       validator.validate_phone])
   about = models.TextField(default="", blank=True)
   image = models.ImageField(
      upload_to=images_upload_to, blank=False)
   bannar = models.ImageField(
      upload_to=images_upload_to, default="profiles/images/banner.jpg")
   gender = models.CharField(max_length=22, choices=gender_choices.choices, null=True, blank=True)
   specialty = models.ManyToManyField(Specialty)
   certified = models.BooleanField(default=False)
   licence = models.FileField(upload_to=licences_upload_to, blank=False)
   Qualification = models.FileField(
      upload_to=qualification_upload_to, blank=False)

   def __str__(self) -> str:
      return f"{self.user.full_name}"
