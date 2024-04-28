# Generated by Django 5.0.3 on 2024-04-28 21:12

import django.db.models.deletion
import service.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=service.models.group_based_upload_to)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to=service.models.service_file_upload_to)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('status', models.CharField(choices=[('accepted', 'مقبول'), ('pending', 'قيد الانتظار'), ('rejected', 'مرفوض')], default='قيد الانتظار', max_length=18)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('customar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customar', to=settings.AUTH_USER_MODEL)),
                ('lawyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lawyer', to=settings.AUTH_USER_MODEL)),
                ('order_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.specialty')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='', max_length=250)),
                ('rate', models.IntegerField(default=None)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='service.service')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('card_name', models.CharField(max_length=50)),
                ('card_number', models.CharField(max_length=15)),
                ('exp_date', models.DateField()),
                ('paied', models.BooleanField(default=False)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.service'),
        ),
    ]
