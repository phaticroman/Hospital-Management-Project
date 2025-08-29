from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib import messages
from accounts.models import DoctorProfile,PatientProfile
from .models import Appointment,PatientDiagnosis,Billing
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin




class MakeAppointmentView(LoginRequiredMixin,View):
    def get(self, request):
        if request.user.role == 'doctor':
            return redirect('homePage')
        patient = get_object_or_404(PatientProfile, user=request.user)
        doctors = DoctorProfile.objects.filter(availability_status=True,user__current_status='apporved').order_by('user__first_name', 'user__last_name')
        return render(request, 'consultation/makeAppointment.html', {'doctors': doctors})

    def post(self, request):
        if request.user.role != 'patient':
            messages.error('only patient can make appointment')
            return redirect('homePage')
        patient = get_object_or_404(PatientProfile, user=request.user)
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        notes = request.POST.get('notes', '')

        if not doctor_id or not appointment_date:
            messages.error(request, "Doctor and appointment date are required.")
            return redirect('MyAppointments')
        doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
        
        if Appointment.objects.filter(patient=patient,doctor=doctor, status__in=['Pending', 'Confirmed']).first():
            messages.error(request, "You already have a pending appointment.")
            return redirect('MyAppointments')
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            notes=notes
        )
        messages.success(request, "Appointment requested successfully.")
        return redirect('MyAppointments')


class MyAppointments(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role == 'patient':
            patient = PatientProfile.objects.get(user=request.user)
            appointments = Appointment.objects.filter(patient=patient).select_related('diagnosis').order_by('-created_at')
        elif request.user.role == 'doctor':
            doctor = DoctorProfile.objects.get(user=request.user)
            appointments = Appointment.objects.filter(doctor=doctor).select_related('diagnosis').order_by('-created_at')
        else:
            appointments = Appointment.objects.all().select_related('diagnosis')
        return render(request, 'consultation/myAppointmentList.html', {'appointments': appointments})
    


class UpdateAppointmentStatusView(LoginRequiredMixin, View):
    def get(self, request, pk, status):
        appointment = Appointment.objects.get(pk=pk)

        if request.user.role != 'doctor' or appointment.doctor.user != request.user:
            messages.error(request, "You are not authorized to update this appointment.")
            return redirect('MyAppointments')

        if status not in ['Confirmed', 'Cancelled']:
            messages.error(request, "Invalid status.")
            return redirect('MyAppointments')

        appointment.status = status
        appointment.save()
        messages.success(request, f"Appointment {status.lower()} successfully.")
        return redirect('MyAppointments')    
    
    
class patientNoteDetail(DetailView):
    model = Appointment
    template_name='consultation/patientNote.html'
    context_object_name = 'patient'
    

class PatientDiagnosisCreateView(LoginRequiredMixin,View):
    def get(self, request, appointment_id):
        if request.user.role != "doctor":
            messages.error(request, "❌ Only doctors can add diagnosis.")
            return redirect("MyAppointments")

        appointment = get_object_or_404(Appointment, id=appointment_id)
        
        return render(request, "diagnosis/diagnosisCreate.html", {"appointment": appointment})

    def post(self, request, appointment_id):
        if request.user.role != "doctor":
            messages.error(request, "❌ Only doctors can add diagnosis.")
            return redirect("MyAppointments")

        appointment = get_object_or_404(Appointment, id=appointment_id)
        doctor = get_object_or_404(DoctorProfile, user=request.user)

        diagnosis_text = request.POST.get("diagnosis")
        treatment_summary = request.POST.get("treatment_summary")
        medicines_prescribed = request.POST.get("medicines_prescribed")
        follow_up_date = request.POST.get("follow_up_date")
        notes = request.POST.get("notes")

        if not diagnosis_text:
            messages.error(request, "Diagnosis is required.")
            return redirect("PatientDiagnosisCreate", appointment_id=appointment_id)

        PatientDiagnosis.objects.update_or_create(
            appointment=appointment,
            defaults={
                "doctor": doctor,
                "diagnosis": diagnosis_text,
                "treatment_summary": treatment_summary,
                "medicines_prescribed": medicines_prescribed,
                "follow_up_date": follow_up_date or None,
                "notes": notes,
            }
        )

        appointment.status = 'Completed'
        appointment.save()

        messages.success(request, "✅ Diagnosis record saved successfully.")
        return redirect("MyAppointments")

class DiagnosisDetail(LoginRequiredMixin,DetailView):
    model = PatientDiagnosis
    template_name='diagnosis/diagnosisDetails.html'
    context_object_name = 'diagnosis'
    


class PatientDiagnosisListView(LoginRequiredMixin,View):
    def get(self, request,patient_id):
        patient = get_object_or_404(PatientProfile,id=patient_id)
        diagnoses = PatientDiagnosis.objects.filter(appointment__patient=patient)
        return render(request,'diagnosis/diagnosesList.html',{'diagnoses':diagnoses})
    
    
class MakeBill(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        appointment_id  = request.GET.get("appointment_id")
        if not appointment_id:
            messages.error(request,"Miss Appointment in the url")
            return redirect('appointmentList')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment Not Found")
            return redirect('appointmentList')
        return render(request,'bills/MakeBill.html',{'appointment':appointment})

    def post(self, request, *args, **kwargs):
        appointment_id  = request.GET.get("appointment_id")
        consultationFee  = request.POST.get('consultationFee')
        medicineCharges  = request.POST.get('medicineCharges')
        testCharges  = request.POST.get('testCharges')
        otherCharges  = request.POST.get('otherCharges')
        totalAmount  = request.POST.get('totalAmount')
        paymentStatus  = request.POST.get('paymentStatus')
        if not appointment_id:
            messages.error(request, "Missing Appointment in the URL")
            return redirect('appointmentList')
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            messages.error(request,"Appointment Not Found")
            return redirect('appointmentList')
        if request.user.role != 'staff':
            messages.error(request,"Only Staff can Make Bill")
            return redirect('appointmentList')
        if Billing.objects.filter(appointment_id=appointment_id).exists():
            messages.error(request, "Bill already exists for this appointment")
            return redirect('appointmentList')
        Billing.objects.create(
            patient = appointment.patient,
            doctor = appointment.doctor,
            appointment = appointment,
            consultationFee = consultationFee,
            medicineCharges = medicineCharges,
            testCharges = testCharges,
            otherCharges = otherCharges,
            totalAmount = totalAmount,
            paymentStatus = paymentStatus
        )
        return redirect('appointmentList')
    
    
class AppointmentListView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        appointments = Appointment.objects.filter(status='Completed').select_related('patient', 'doctor').order_by('-created_at')
        appointments = appointments.prefetch_related('diagnosis', 'billing').order_by('-created_at')


        context = {
            'appointments': appointments
        }
        return render(request, 'bills/appointmentList.html', context)
    
    
class BillsDetail(LoginRequiredMixin,DetailView):
    model = Billing
    template_name='bills/billDetails.html'