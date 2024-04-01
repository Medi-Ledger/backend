from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    TYPE_CHOICES = (
        ('doctor', 'doctor'),
        ('patient', 'patient'),
    )
    email = models.EmailField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='patient')
    adhaar = models.CharField(max_length=20, null=True, blank=True)
    mrn = models.CharField(max_length=10, null=True, blank=True)


class Record(models.Model):
    TYPE_CHOICES = (
        ('file', 'file'),
        ('text', 'text'),
        ('image', 'image'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    data = models.JSONField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)


class Block(models.Model):
    parent = models.CharField(max_length=256)
    current = models.CharField(max_length=256)
    record1 = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='first')
    record2 = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='second')
    record3 = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='third')
    record4 = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='fourth')
    record5 = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='fifth')