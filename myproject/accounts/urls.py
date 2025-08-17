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
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctorDetail'),
    path('doctor/profile/update/', DoctorProfileUpdateView.as_view(), name='doctorProfileUpdate'),
    
    
    path('patientDetails/<int:pk>/', PatientDetailView.as_view(), name='patientDetail'),
    path('patientDetails/<int:pk>/update/', PatientUpdateView.as_view(), name='patientUpdateView'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
