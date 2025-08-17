from django.contrib import admin
from .models import CustomUser,DoctorProfile,PatientProfile

admin.site.register(CustomUser)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
