from django.contrib import admin
from .models import User, Record, Block, Diagnosis

admin.site.register(User)
admin.site.register(Record)
admin.site.register(Block)
admin.site.register(Diagnosis)
