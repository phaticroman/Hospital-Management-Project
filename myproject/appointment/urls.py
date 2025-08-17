from django.urls import path
from .views import MakeAppointmentView,MyAppointments,UpdateAppointmentStatusView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('make/', MakeAppointmentView.as_view(), name='appointmentMakeAppointment'),
    path('MyAppointments/', MyAppointments.as_view(), name='MyAppointments'),
    path('appointment/<int:pk>/status/<str:status>/', UpdateAppointmentStatusView.as_view(), name='updateAppointmentStatus'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
