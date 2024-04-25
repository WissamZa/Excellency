from django.db import models

legal_advice = "استشارات قانونية"
drafting_contracts = "صياغة عقود"
warrant = "مذكرات"

Specialty_CHOICES = {
    'legal_advice': legal_advice,
    'drafting_contracts': drafting_contracts,
    'warrant': warrant
}


class Specialty(models.Model):
   name = models.CharField(max_length=20)
