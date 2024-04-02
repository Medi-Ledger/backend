from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import hash

class User(AbstractUser):
    TYPE_CHOICES = (
        ('doctor', 'doctor'),
        ('patient', 'patient'),
    )
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=50)
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
    created_at = models.DateTimeField(auto_now_add=True)

class Diagnosis(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    record = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='diagnosis')

class Block(models.Model):
    parent = models.CharField(max_length=256)
    hash = models.CharField(max_length=256)
    record1 = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='first')
    record2 = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='second')
    record3 = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='third')
    record4 = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='fourth')
    record5 = models.ForeignKey(Record, on_delete=models.SET_NULL, null=True, blank=True, related_name='fifth')
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Block ID: {self.hash} | Block Size: {str(self.count)}'

    @classmethod
    def get_latest_block(cls):
        block = cls.objects.last()
        if block.count == 5:
            return cls.add_block(block)
        return block

    @classmethod
    def add_block(cls, parent=None):
        if not parent:
            parent = cls.objects.last()
        if parent.count != 5:
            raise Exception("Current block is not full")
        return cls.objects.create(parent=parent.hash, current='ffffffffffffffff')

    @classmethod
    def add_record(cls, record):
        block = cls.get_latest_block()
        block.add_record_to_block(record)

    def add_record_to_block(self, record):
        self.count += 1

        field = f'record{self.count}'
        setattr(self, field, record)

        name_string = ''
        for i in range(self.count):
            name_string += getattr(self, f'record{i+1}').name
            print(i, getattr(self, f'record{i+1}').name)
        print(name_string)
        new_hash = hash(name_string)
        self.hash = new_hash
        self.save()


@receiver(post_save, sender=Record)
def create_block_if_needed(sender, instance, created, **kwargs):
    if created:
        Block.add_record(instance)

'''shell script - Genesis Block
from record.models import Block
block = Block.objects.create(parent='0000000000000000', hash='ffffffffffffffff')
'''

'''shell script - Create Record
from record.models import Block, Record, User
user = User.objects.first()
rec = Record.objects.create(user=user, type='text', name='test')
Block.add_record(rec)
'''