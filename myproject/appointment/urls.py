from django.urls import path
from .views import MakeAppointmentView,MyAppointments,UpdateAppointmentStatusView,patientNoteDetail,PatientDiagnosisCreateView,DiagnosisDetail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('make/', MakeAppointmentView.as_view(), name='createAppointment'),
    path('MyAppointments/', MyAppointments.as_view(), name='MyAppointments'),
    path('patientNoteDetail/<int:pk>', patientNoteDetail.as_view(), name='patientNoteDetail'),
    path('DiagnosisDetail/<int:pk>', DiagnosisDetail.as_view(), name='DiagnosisDetail'),
    path('appointment/<int:pk>/status/<str:status>/', UpdateAppointmentStatusView.as_view(), name='updateAppointmentStatus'),
    path('diagnosis/create/<int:appointment_id>/', PatientDiagnosisCreateView.as_view(), name='PatientDiagnosisCreate'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
