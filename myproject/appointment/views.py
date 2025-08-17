from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib import messages
from accounts.models import DoctorProfile,PatientProfile
from .models import Appointment
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin




class MakeAppointmentView(LoginRequiredMixin,View):
    def get(self, request):
        patient = get_object_or_404(PatientProfile, user=request.user)
        doctors = DoctorProfile.objects.filter(availability_status=True)
        return render(request, 'consultation/makeAppointment.html', {'doctors': doctors})

    def post(self, request):
        patient = get_object_or_404(PatientProfile, user=request.user)
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        notes = request.POST.get('notes', '')

        if not doctor_id or not appointment_date:
            messages.error(request, "Doctor and appointment date are required.")
            return redirect('createAppointment')
        doctor = get_object_or_404(DoctorProfile, pk=doctor_id)
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            notes=notes
        )
        messages.success(request, "Appointment requested successfully.")
        return redirect('MyAppointments')


class MyAppointments(LoginRequiredMixin,View):
    def get(self,request):
        if request.user.role == 'patient':
            patient = PatientProfile.objects.get(user=request.user)
            appointments = Appointment.objects.filter(patient=patient)
        elif request.user.role == 'doctor':
            doctor = DoctorProfile.objects.get(user=request.user)
            appointments = Appointment.objects.filter(doctor=doctor)
        else:
            appointments = Appointment.objects.all()
        return render(request,'consultation/myAppointmentList.html',{'appointments':appointments})
    


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