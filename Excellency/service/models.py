from django.db import models
from account.models import User, Specialty

legal_advice = "استشارات قانونية"
drafting_contracts = "صياغة عقود"
warrant = "مذكرات"

Specialty_CHOICES = {
    'legal_advice': legal_advice,
    'drafting_contracts': drafting_contracts,
    'warrant': warrant
}


def service_file_upload_to(instance, filename):
   return "service/file/{}/{}".format(instance.user.id, filename)


class Service(models.Model):
   completed = "مكتمل"
   accepted = "مقبول"
   pending_accept_offer = "انتظار قبول السعر"
   pending = "قيد الانتظار"
   rejected = "مرفوض"
   STATUS_CHOICES = (
      ('completed', completed),
       ('accepted', accepted),
       ('pending_accept_offer', pending_accept_offer),
       ('pending', pending),
       ('rejected', rejected),
    )
   lawyer = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name="lawyer")
   customar = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name="customar")
   order_type = models.ForeignKey(Specialty, on_delete=models.CASCADE)
   subject = models.CharField(max_length=100)
   content = models.TextField()
   file = models.FileField(
      upload_to=service_file_upload_to, blank=True, null=True)
   price = models.FloatField(
       blank=True, null=True)
   status = models.CharField(
      max_length=18, default=pending)
   created_date = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
   service = models.ForeignKey(Service, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   content = models.TextField()
   added_date = models.DateTimeField(auto_now_add=True)


def group_based_upload_to(instance, filename):
   return "profiles/file/{}/{}".format(instance.user.id, filename)


class Files(models.Model):
   comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   file = models.FileField(upload_to=group_based_upload_to)


class Payment(models.Model):
   service = models.ForeignKey(Service, on_delete=models.CASCADE)
   total_price = models.DecimalField(max_digits=5, decimal_places=2)
   card_name = models.CharField(max_length=50)
   card_number = models.CharField(max_length=15)
   exp_date = models.DateField()
   paied = models.BooleanField(default=False)


class Rating(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   service = models.OneToOneField(Service, on_delete=models.CASCADE)
   comment = models.TextField(max_length=250, default="")
   rate = models.IntegerField(default=None)
