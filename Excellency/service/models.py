from django.db import models
from account.models import User, Specialty


class Service(models.Model):
   accepted = "مقبول"
   pending = "قيد الانتظار"
   rejected = "مرفوض"
   STATUS_CHOICES = (
       ('accepted', accepted),
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
   price = models.DecimalField(decimal_places=2, max_digits=4)
   status = models.CharField(max_length=18, choices=STATUS_CHOICES)
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
   payed = models.BooleanField(default=False)
