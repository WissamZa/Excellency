from django.db import models


class Specialty_choice(models.TextChoices):
   legal_advice = "استشارات قانونية"
   drafting_contracts = "صياغة عقود"
   warrant = "مذكرات"


class Specialty(models.Model):
   name = models.CharField(max_length=20, choices=Specialty_choice.choices,)
