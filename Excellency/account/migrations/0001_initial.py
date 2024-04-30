# Generated by Django 5.0.3 on 2024-04-30 08:32

import account.models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import main.validator
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0014_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('national_id', models.CharField(max_length=10, unique=True, validators=[main.validator.validate_national_id])),
                ('email', models.EmailField(max_length=100, unique=True, validators=[main.validator.validate_email])),
                ('full_name', models.CharField(max_length=50)),
                ('role', models.CharField(blank=True, choices=[('Supervisor', 'ادارة'), ('Lawyer', 'محامي'), ('Customar', 'عميل')], max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CustomarProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=10, validators=[main.validator.validate_phone])),
                ('image', models.ImageField(default='/profiles/images/user-default.png', upload_to=account.models.images_upload_to)),
                ('bannar', models.ImageField(default='/profiles/images/banner.jpg', upload_to=account.models.images_upload_to)),
                ('gender', models.CharField(blank=True, choices=[('ذكر', 'Male'), ('انثى', 'Female')], max_length=22, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customar_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LawyerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10, unique=True, validators=[main.validator.validate_phone])),
                ('about', models.TextField(blank=True, default='')),
                ('image', models.ImageField(upload_to=account.models.images_upload_to)),
                ('bannar', models.ImageField(default='profiles/images/banner.jpg', upload_to=account.models.images_upload_to)),
                ('gender', models.CharField(blank=True, choices=[('ذكر', 'Male'), ('انثى', 'Female')], max_length=22, null=True)),
                ('certified', models.BooleanField(default=False)),
                ('licence', models.FileField(upload_to=account.models.licences_upload_to)),
                ('Qualification', models.FileField(upload_to=account.models.qualification_upload_to)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lawyer_profile', to=settings.AUTH_USER_MODEL)),
                ('specialty', models.ManyToManyField(to='account.specialty')),
            ],
        ),
    ]
