from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('make/', MakeAppointmentView.as_view(), name='createAppointment'),
    path('MyAppointments/', MyAppointments.as_view(), name='MyAppointments'),
    path('patientNoteDetail/<int:pk>', patientNoteDetail.as_view(), name='patientNoteDetail'),
    path('appointment/<int:pk>/status/<str:status>/', UpdateAppointmentStatusView.as_view(), name='updateAppointmentStatus'),
    
    path('diagnosis/create/<int:appointment_id>/', PatientDiagnosisCreateView.as_view(), name='PatientDiagnosisCreate'),
    path('DiagnosisDetail/<int:pk>', DiagnosisDetail.as_view(), name='DiagnosisDetail'),
    path("appointment/PatientDiagnosisList/<int:patient_id>/", PatientDiagnosisListView.as_view(), name="PatientDiagnosisList"),
    
    
    path("MakeBill/", MakeBill.as_view(), name="MakeBill"),
    path("AppointmentListView/", AppointmentListView.as_view(), name="AppointmentListView"),
    path("BillsDetail/<int:pk>", BillsDetail.as_view(), name="BillsDetail"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
