from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import re


def validate_national_id(value):

   return re.match(r'^1[0-9]{9}$', value)


def validate_password(value):
   if not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$', value):
      raise ValidationError('كلمة مرور غير صالحة')


def validate_email(value):
   EmailValidator(
       message="البريد الالكتروني غير صحيح")(value)


def validate_phone(value):
   if not re.match('^05[0-9]{4}[0-9]{4}$', value):
      raise ValidationError(
          'رقم الهاتف يجب ان يكون مكون من 10 ارقام و ان يبدأ بـ 05')


def validat(**keywords):
   for key, value in keywords.items():
      match key:
         case "full_name":
            if not (len(str(value).split(" ")) >= 3):
               raise ValidationError("يرجى كتابة الإسم الثلاثي")

         case "national_id":
            if not validate_national_id(value):
               raise ValidationError("رقم الهوية غير صالح")

         case "phone":
            validate_phone(value)

         case "email":
            validate_email(value)

         case "password":
            validate_password(value)

         case _:
            raise NotImplementedError()

      return value
