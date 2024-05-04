from rest_framework import serializers
from .models import User, Record, Block, Node

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'name']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'mrn', 'password', 'name']

class DataUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['name', 'data']

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['name', 'file']

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['name', 'image']

class DoctorDataUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['user', 'name', 'data']

class DoctorFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['user', 'name', 'file']

class DoctorImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['user', 'name', 'image']

class RecordDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'

class BlockSerializer(serializers.ModelSerializer):
    record1 = RecordDataSerializer()
    record2 = RecordDataSerializer()
    record3 = RecordDataSerializer()
    record4 = RecordDataSerializer()
    record5 = RecordDataSerializer()

    class Meta:
        model = Block
        fields = '__all__'

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'