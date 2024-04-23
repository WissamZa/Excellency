from django.db import models
from main import validator


class Contactus(models.Model):
   full_name = models.CharField(max_length=50, blank=False)
   email = models.EmailField(blank=False, validators=[
                             validator.validate_email])
   subject = models.CharField(max_length=120, blank=False)
   message = models.TextField(blank=False)
   created_at = models.DateTimeField(auto_now_add=True)
