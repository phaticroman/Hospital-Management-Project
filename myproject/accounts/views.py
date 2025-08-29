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
from django.contrib.auth.decorators import login_required
@login_required
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
            if user.role == 'admin':
                return redirect('adminDashboard')
            elif user.role == 'doctor':
                if DoctorProfile.objects.filter(user=user).exists():
                    return redirect('doctorprofile')
                else:
                    return redirect('doctorProfileUpdate')
            elif user.role == 'patient':
                if PatientProfile.objects.filter(user=user).exists():
                    return redirect('PatientProfileView')
                else:
                    return redirect('patientUpdateView')
            elif user.role == 'staff':
                if StaffProfile.objects.filter(user=user).exists():
                    return redirect('StaffProfileView')
                else:
                    return redirect('StaffUpdateView')
        else:
            messages.error(request, "❌ Invalid username or password.")
            return redirect('loginPage')


class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "👋 You have been logged out.")
        return redirect('loginPage')

@login_required
def deleteUser(request,pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.user.role != 'admin' and request.user != user:
        messages.error('only admin Can delete an account')
        if request.user.role == 'admin':
            return redirect('adminDashboard')
        return redirect('doctorprofile')
    user = get_object_or_404(CustomUser, pk=pk)
    user.delete()
    if request.user.role == 'admin':
        return redirect('adminDashboard')
    return redirect('loginPage')

#doctor List
class DoctorListView(LoginRequiredMixin,View):
    
    def get(self, request):
        doctors = DoctorProfile.objects.filter(user__current_status='apporved')
        return render(request,'doctor/doctorList.html',{'doctors':doctors})
    
#doctor Details
class DoctorDetailView(LoginRequiredMixin,DetailView):
    model = DoctorProfile
    template_name='doctor/doctorDetail.html'
    context_object_name = "doctor"
    
    
#Doctor Profile Update
class DoctorProfileUpdateView(LoginRequiredMixin,View):
    def get(self, request):
        doctor, created = DoctorProfile.objects.get_or_create(user=request.user)
        return render(request, 'doctor/doctorProfileUpdate.html', {'doctor': doctor})

    def post(self, request):
        doctor, created = DoctorProfile.objects.get_or_create(user=request.user)

        contact_number = request.POST.get('contact_number', doctor.contact_number)
        department = request.POST.get('department', doctor.department)
        specialization = request.POST.get('specialization', doctor.specialization)
        qualification = request.POST.get('qualification', doctor.qualification)
        experience = request.POST.get('experience', doctor.experience)
        consultation_fee = request.POST.get('consultation_fee', doctor.consultation_fee)
        bio = request.POST.get('bio', doctor.bio)
        availability_status = True if request.POST.get('availability_status') == 'on' else False

        if not all([contact_number, department, specialization, qualification, experience, consultation_fee, bio]):
            messages.error(request, "All fields are required.")
            return redirect('doctorProfileUpdate')
        doctor.contact_number = contact_number
        doctor.department = department
        doctor.specialization = specialization
        doctor.qualification = qualification
        doctor.experience = experience
        doctor.consultation_fee = consultation_fee
        doctor.bio = bio
        doctor.availability_status = availability_status
        if request.FILES.get('profile_picture'):
            doctor.profile_picture = request.FILES['profile_picture']
        doctor.save()
        messages.success(request, "✅ Your profile has been updated successfully.")
        return redirect('doctorprofile')
        

class DoctorProfileView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.user.role == 'doctor':
            profile = get_object_or_404(DoctorProfile, user=request.user)
        return render(request,'doctor/doctorProfile.html',{'profile':profile})
          

class PatientDetailView(LoginRequiredMixin,DetailView):
    model = PatientProfile
    template_name='patient/patientDetail.html'
    context_object_name = 'patient'
    
class PatientUpdateView(LoginRequiredMixin,View):
    def get(self, request):
        patient,created = PatientProfile.objects.get_or_create(user=request.user)
        doctors = DoctorProfile.objects.all()
        return render(request, 'patient/patientUpdateView.html', {'patient': patient, 'doctors': doctors})

    def post(self, request):
        patient,created = PatientProfile.objects.get_or_create(user=request.user)

        gender = request.POST.get('gender', patient.gender)
        date_of_birth = request.POST.get('date_of_birth', patient.date_of_birth)
        contact_number = request.POST.get('contact_number', patient.contact_number)
        address = request.POST.get('address', patient.address)
        blood_group = request.POST.get('blood_group', patient.blood_group)
        allergies = request.POST.get('allergies', patient.allergies)
        emergency_contact_number = request.POST.get('emergency_contact', patient.emergency_contact_number)
        status = request.POST.get('status', patient.status)
        if not all([gender,date_of_birth,contact_number,address,blood_group,allergies,emergency_contact_number]):
            messages.error(request, "All fields are required.")
            return redirect('patientUpdateView')
        patient.gender = gender
        patient.date_of_birth = date_of_birth
        patient.contact_number = contact_number
        patient.address = address
        patient.blood_group = blood_group
        patient.allergies = allergies
        patient.emergency_contact_number = emergency_contact_number
        patient.status = status
        if request.FILES.get('profile_picture'):
            patient.profile_picture = request.FILES['profile_picture']
        
        patient.save()
        messages.success(request, "✅ Patient profile updated successfully.")
        return redirect('homePage')
    
    

class PatientProfileView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.user.role == 'patient':
            profile = get_object_or_404(PatientProfile, user=request.user)
        return render(request,'patient/patientProfile.html',{'profile':profile})



#staff
class StaffUpdateView(LoginRequiredMixin,View):
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
    
    
    
    
class StaffProfileView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        if request.user.role == 'staff':
            profile = get_object_or_404(StaffProfile, user=request.user)
        return render(request,'staff/staffProfile.html',{'profile':profile})
    
    
    
#admin
class PandingUserView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        allusers = CustomUser.objects.filter(current_status='pending')
        return render(request,'admin/pandingUserList.html',{'allusers':allusers})



class UpdateUserStatusView(LoginRequiredMixin,View):
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
        

class adminDashboard(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        context = {
        "total_doctors": DoctorProfile.objects.filter(user__current_status='apporved').count(),
        "total_patients": PatientProfile.objects.count(),
        "total_staff": StaffProfile.objects.filter(user__current_status='apporved').count(),
        "total_appointments": Appointment.objects.count(),
        "recent_appointments": Appointment.objects.order_by('-created_at')[:5],
        "recent_bills": Billing.objects.order_by('-billDate')[:5],
        "panding_users": CustomUser.objects.filter(current_status="panding"),
    }

        return render(request, "admin/adminDashboard.html",context)
    

@login_required
def doctorListForAdmin(request):
    doctors = CustomUser.objects.filter(role='doctor').order_by('-id')
    return render(request,'admin/doctorListForAdmin.html',{'doctors':doctors})

@login_required
def patientListForAdmin(request):
    patient = CustomUser.objects.filter(role='patient').order_by('-id')
    return render(request,'admin/patientListForAdmin.html',{'patient':patient})
@login_required
def staffListForAdmin(request):
    staff = CustomUser.objects.filter(role='staff').order_by('-id')
    return render(request,'admin/staffListForAdmin.html',{'staff':staff})

@login_required
def billListForAdmin(request):
    bills = Billing.objects.order_by('-billDate')
    return render(request,'admin/billListForAdmin.html',{'bills':bills})