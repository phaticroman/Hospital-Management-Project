from django.contrib import admin
from .models import CustomUser,DoctorProfile,PatientProfile,StaffProfile

admin.site.register(CustomUser)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(StaffProfile)

