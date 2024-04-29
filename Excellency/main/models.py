from django.db import models
from main import validator
from account.models import User

class Contactus(models.Model):
   full_name = models.CharField(max_length=50, blank=False)
   email = models.EmailField(blank=False, validators=[
                             validator.validate_email])
   subject = models.CharField(max_length=120, blank=False)
   message = models.TextField(blank=False)
   created_at = models.DateTimeField(auto_now_add=True)
   
def post_image_upload_to(instance, filename):
   return "post/images/{}/{}".format(instance.author.id, filename)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=post_image_upload_to, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title