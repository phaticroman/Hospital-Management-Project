from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib import messages
from .models import DoctorProfile,PatientProfile,StaffProfile
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from appointment.models import *

def homePage(request):
    return render(request,'homePage.html')

CustomUser = get_user_model()

class SignUpView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get('username')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')

        if not all([username, password, email, role,lastName,firstName]):
            messages.error(request, "⚠️ All fields are required.")
            return redirect('signupPage')

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "⚠️ Username already exists.")
            return redirect('signupPage')
        if role == 'patient':
            status = 'approved'
        else :
            status = 'panding'
        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            role=role,
            first_name=firstName,
            last_name=lastName,
            current_status=status,
        )
        if role == 'doctor':
            DoctorProfile.objects.create(user=user)
            messages.success(request, "👨‍⚕️ Doctor created successfully.")
        elif role == 'patient':
            PatientProfile.objects.create(user=user)
            messages.success(request, "👨‍⚕️ Patient created successfully.")
        elif role == 'staff':
            StaffProfile.objects.create(user=user)
            messages.success(request, "👨‍⚕️ Staff created successfully.")
        login(request, user)
        messages.success(request, "🎉 Account created successfully! Please log in.")
        return redirect('loginPage')


class CustomLogin(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"✅ Welcome back, {username}!")
            return redirect('homePage')
        else:
            messages.error(request, "❌ Invalid username or password.")
            return redirect('loginPage')


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "👋 You have been logged out.")
        return redirect('loginPage')
    

#doctor List
class DoctorListView(View):
    def get(self, request):
        doctors = DoctorProfile.objects.filter(user__current_status='apporved')
        return render(request,'doctor/doctorList.html',{'doctors':doctors})
    
#doctor Details
class DoctorDetailView(DetailView):
    model = DoctorProfile
    template_name='doctor/doctorDetail.html'
    context_object_name = "doctor"
    
    
#Doctor Profile Update
class DoctorProfileUpdateView(View):
    def get(self, request):
        doctor = get_object_or_404(DoctorProfile, user=request.user)
        return render(request, 'doctor/doctorProfileUpdate.html', {'doctor': doctor})

    def post(self, request):
        doctor = get_object_or_404(DoctorProfile, user=request.user)

        doctor.contact_number = request.POST.get('contact_number', doctor.contact_number)
        doctor.department = request.POST.get('department', doctor.department)
        doctor.specialization = request.POST.get('specialization', doctor.specialization)
        doctor.qualification = request.POST.get('qualification', doctor.qualification)
        doctor.experience = request.POST.get('experience', doctor.experience)
        doctor.consultation_fee = request.POST.get('consultation_fee', doctor.consultation_fee)
        doctor.bio = request.POST.get('bio', doctor.bio)
        doctor.availability_status = True if request.POST.get('availability_status') == 'on' else False


        if request.FILES.get('profile_picture'):
            doctor.profile_picture = request.FILES['profile_picture']

        doctor.save()
        messages.success(request, "✅ Your profile has been updated successfully.")
        return redirect('doctorprofile')
        

class DoctorProfileView(View):
    def get(self, request, *args, **kwargs):
        if request.user.role == 'doctor':
            profile = get_object_or_404(DoctorProfile, user=request.user)
        return render(request,'doctor/doctorProfile.html',{'profile':profile})
          

class PatientDetailView(DetailView):
    model = PatientProfile
    template_name='patient/patientDetail.html'
    context_object_name = 'patient'
    
class PatientUpdateView(View):
    def get(self, request, pk):
        patient = get_object_or_404(PatientProfile, pk=pk)
        doctors = DoctorProfile.objects.all()
        return render(request, 'patient/patientUpdateView.html', {'patient': patient, 'doctors': doctors})

    def post(self, request, pk):
        patient = get_object_or_404(PatientProfile, pk=pk)

        patient.gender = request.POST.get('gender', patient.gender)
        patient.date_of_birth = request.POST.get('date_of_birth', patient.date_of_birth)
        patient.contact_number = request.POST.get('contact_number', patient.contact_number)
        patient.address = request.POST.get('address', patient.address)
        patient.blood_group = request.POST.get('blood_group', patient.blood_group)
        patient.allergies = request.POST.get('allergies', patient.allergies)
        patient.emergency_contact_number = request.POST.get('emergency_contact', patient.emergency_contact_number)
        doctor_id = request.POST.get('doctor_assigned')
        patient.doctor_assigned = DoctorProfile.objects.get(pk=doctor_id) if doctor_id else None
        patient.status = request.POST.get('status', patient.status)

        if request.FILES.get('profile_picture'):
            patient.profile_picture = request.FILES['profile_picture']

        patient.save()
        messages.success(request, "✅ Patient profile updated successfully.")
        return redirect('homePage')
    
    

class PatientProfileView(View):
    def get(self, request, *args, **kwargs):
        if request.user.role == 'patient':
            profile = get_object_or_404(PatientProfile, user=request.user)
        return render(request,'patient/patientProfile.html',{'profile':profile})




class StaffUpdateView(View):
    def get(self, request, pk):
        staff = get_object_or_404(StaffProfile, pk=pk)
        return render(request, 'staff/staffUpdateView.html', {'staff': staff})

    def post(self, request, pk):
        staff = get_object_or_404(StaffProfile, pk=pk)

        staff.role = request.POST.get('role', staff.role)
        staff.contactNumber = request.POST.get('contactNumber', staff.contactNumber)
        staff.address = request.POST.get('address', staff.address)
        staff.shiftTime = request.POST.get('shiftTime', staff.shiftTime)
        staff.salary = request.POST.get('salary', staff.salary)

        if request.FILES.get('profile_picture'):
            staff.profile_picture = request.FILES['profile_picture']

        staff.save()
        messages.success(request, "✅ Staff profile updated successfully.")
        return redirect('homePage')
    
    
    
    
class StaffProfileView(View):
    def get(self, request, *args, **kwargs):
        if request.user.role == 'staff':
            profile = get_object_or_404(StaffProfile, user=request.user)
        return render(request,'staff/staffProfile.html',{'profile':profile})
    
    
    

class PandingUserView(View):
    def get(self, request, *args, **kwargs):
        allusers = CustomUser.objects.filter(current_status='pending')
        return render(request,'admin/pandingUserList.html',{'allusers':allusers})



class UpdateAppointmentStatusView(LoginRequiredMixin,View):
    def get(self, request, pk,current_status):
        panding_user = CustomUser.objects.get(pk=pk)
        
        if request.user.role != 'admin':
            messages.error(request, "You are not authorized to update this appointment.")
            return redirect('adminDashboard')
        if current_status not in ['cancel', 'apporved']:
            messages.error(request, "Invalid status.")
            return redirect('adminDashboard')
        panding_user.current_status = current_status
        panding_user.save()
        messages.success(request, f"User {current_status.lower()} successfully.")
        return redirect('adminDashboard')
        

class adminDashboard(View):
    def get(self, request, *args, **kwargs):
        context = {
        "total_doctors": DoctorProfile.objects.count(),
        "total_patients": PatientProfile.objects.count(),
        "total_staff": StaffProfile.objects.count(),
        "total_appointments": Appointment.objects.count(),
        "recent_appointments": Appointment.objects.order_by('-created_at')[:5],
        "recent_bills": Billing.objects.order_by('-billDate')[:5],
        "panding_users": CustomUser.objects.filter(current_status="panding"),
    }

        return render(request, "admin/adminDashboard.html",context)