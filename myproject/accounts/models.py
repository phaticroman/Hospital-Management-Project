from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('staff', 'Staff'),
    )
    CURRENT_STATUS = [
        ('apporved','Approved'),
        ('panding','Panding'),
        ('cancel','Cancel'),
    ]
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)
    role = models.CharField(choices=ROLE_CHOICES, max_length=50,null=True, blank=True)
    current_status = models.CharField(choices=CURRENT_STATUS, max_length=50,default='panding')
    
class DoctorProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pediatrics', 'Pediatrics'),
        ('General', 'General'),
        ('Dermatology', 'Dermatology'),
        ('Gynecology', 'Gynecology'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, default='General')
    specialization = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True,blank=True)
    experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    availability_status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.first_name


class PatientProfile(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    STATUS_CHOICES = [
        ('Outpatient', 'Outpatient'),
        ('Inpatient', 'Inpatient'),
        ('Discharged', 'Discharged'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='patient_profiles/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    allergies = models.TextField(null=True, blank=True)

    emergency_contact_number = models.CharField(max_length=15, null=True, blank=True)

    doctor_assigned = models.ForeignKey('DoctorProfile', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Outpatient')

    def __str__(self):
        return self.user.username



class StaffProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='Staff_profiles/', null=True, blank=True)
    role = models.CharField(max_length=50)
    joinDate = models.DateField(auto_now_add=True)
    contactNumber = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    shiftTime = models.CharField(max_length=50, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"
