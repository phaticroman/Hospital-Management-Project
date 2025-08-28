from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',homePage,name='homePage'),
    path('loginPage/',CustomLogin.as_view(),name='loginPage'),
    path('signup/',SignUpView.as_view(),name='signupPage'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
    
    path('doctors/', DoctorListView.as_view(), name='doctorList'),
    path('doctorprofile/', DoctorProfileView.as_view(), name='doctorprofile'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctorDetail'),
    path('doctor/profile/update/', DoctorProfileUpdateView.as_view(), name='doctorProfileUpdate'),
    
    
    path('patientDetails/<int:pk>/', PatientDetailView.as_view(), name='patientDetail'),
    path('PatientProfileView/', PatientProfileView.as_view(), name='PatientProfileView'),
    path('patientDetail/<int:pk>/update/', PatientUpdateView.as_view(), name='patientUpdateView'),
    
    path('StaffUpdateView/<int:pk>/', StaffUpdateView.as_view(), name='StaffUpdateView'),
    path('StaffProfileView/', StaffProfileView.as_view(), name='StaffProfileView'),
    
    
    path('adminDashboard/', adminDashboard.as_view(), name='adminDashboard'),
    path('UpdateAppointmentStatusView/<int:pk>/status/<str:current_status>/', UpdateAppointmentStatusView.as_view(), name='UpdateAppointmentStatusView'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
