from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('patient/register/', views.PatientRegisterView.as_view(), name='patient-register'),
    path('patient/data/', views.DataUploadView.as_view(), name='patient-data'),
    path('patient/image/', views.ImageUploadView.as_view(), name='patient-image'),
    path('patient/file/', views.FileUploadView.as_view(), name='patient-file'),
    path('patient/history/', views.PatientHistoryView.as_view(), name='patient-history'),
    path('doctor/register/', views.DoctorRegisterView.as_view(), name='doctor-register'),
    path('doctor/diagnosis/', views.DoctorPatientsView.as_view(), name='doctor-diagnosis'),
    path('doctor/lookup/', views.PatientLookupView.as_view(), name='patient-lookup'),
    path('doctor/data/', views.DoctorDataUploadView.as_view(), name='doctor-data'),
    path('doctor/image/', views.DoctorImageUploadView.as_view(), name='doctor-image'),
    path('doctor/file/', views.DoctorFileUploadView.as_view(), name='doctor-file'),
    path('doctor/history/', views.DoctorPatientHistoryView.as_view(), name='doctor-history'),
]
