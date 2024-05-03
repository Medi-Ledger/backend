from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .models import User, Diagnosis, Record
from .serializers import (
    DoctorSerializer,
    PatientSerializer,
    DataUploadSerializer,
    FileUploadSerializer,
    ImageUploadSerializer,
    DoctorDataUploadSerializer,
    DoctorFileUploadSerializer,
    DoctorImageUploadSerializer,
    RecordDataSerializer,
)

class PatientRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data.get('username', ''),
                password=request.data.get('password', ''),
                type='patient',
                adhaar=request.data.get('username', ''),
                name=request.data.get('name')
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data.get('username', ''),
                password=request.data.get('password', ''),
                type='doctor',
                mrn=request.data.get('username', ''),
                name = request.data.get('name')
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'detail': 'invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class DataUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DataUploadSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            name = request.data['name']
            data = request.data['data']
            record = Record.objects.create(user=user, name=name, data=data, type='text')
            return Response({'id': record.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        print(request.data)
        print(request.FILES)
        if serializer.is_valid():
            user = request.user
            name = request.data['name']
            file = request.FILES['file']
            record = Record.objects.create(user=user, name=name, file=file, type='file')
            return Response({'id': record.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            name = request.data['name']
            image = request.FILES['image']
            record = Record.objects.create(user=user, name=name, image=image, type='image')
            return Response({'id': record.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorDataUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DoctorDataUploadSerializer(data=request.data)
        if serializer.is_valid() and request.user.type == 'doctor':
            user_id = request.data['user']
            name = request.data['name']
            data = request.data['data']
            record = Record.objects.create(user_id=user_id, name=name, data=data, type='data')
            diag = Diagnosis.objects.create(patient_id=user_id, doctor=request.user, record=record)
            return Response({'id': record.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorFileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DoctorFileUploadSerializer(data=request.data)
        if serializer.is_valid() and request.user.type == 'doctor':
            user_id = request.data['user']
            name = request.data['name']
            file = request.FILES['file']
            record = Record.objects.create(user_id=user_id, name=name, file=file, type='file')
            diag = Diagnosis.objects.create(patient_id=user_id, doctor=request.user, record=record)
            return Response({'id': record.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorImageUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DoctorImageUploadSerializer(data=request.data)
        if serializer.is_valid() and request.user.type == 'doctor':
            user_id = request.data['user']
            name = request.data['name']
            image = request.FILES['image']
            record = Record.objects.create(user_id=user_id, name=name, image=image, type='image')
            diag = Diagnosis.objects.create(patient_id=user_id, doctor=request.user, record=record)
            return Response({'id': record.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientLookupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = request.data.get('username', '')
        try:
            patient_id = User.objects.get(username=username, type='patient').id
            return Response({'patient_id': patient_id}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

class DoctorPatientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.type == 'doctor':
            patients = User.objects.filter(doctors__doctor=request.user).distinct('id')
            patient_data = [{'id': patient.id, 'username': patient.username, 'name': patient.name} for patient in patients]
            return Response(patient_data, status=status.HTTP_200_OK)
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

class PatientHistoryView(APIView):
    def get(self, request):
        user = request.user
        records = Record.objects.filter(user=user)
        serializer = RecordDataSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DoctorPatientHistoryView(APIView):
    def post(self, request):
        if request.user.type != 'doctor':
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

        patient_id = request.data.get('user', None)
        if patient_id is None:
            return Response({'error': 'Patient ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = User.objects.get(id=patient_id, type='patient')
        except User.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        records = Record.objects.filter(user=patient)
        serializer = RecordDataSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

