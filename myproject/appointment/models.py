from django.db import models
from django.utils import timezone
from accounts.models import DoctorProfile, PatientProfile

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.doctor.user.get_full_name()} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"
    
    

class PatientDiagnosis(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE,related_name="diagnosis",null=True,blank=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    treatment_summary = models.TextField(null=True, blank=True)
    medicines_prescribed = models.TextField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Diagnosis for {self.appointment.patient.user.get_full_name()}"
