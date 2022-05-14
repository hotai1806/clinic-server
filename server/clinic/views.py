from django.shortcuts import render
from rest_framework import viewsets, status, permissions, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes


from .models import Appointment, Diagnostician,\
    PrescriptionItem, Medicine, Prescription, ScheduleTask
from clinic.serializers import AppointmentSerializer, DiagnosticianSerializer,\
    PrescriptionItemSerializer, MedicineSerializer, PrescriptionSerializer, ScheduleTaskSerializer
# Create your views here.


class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    http_method_names = ['get', 'patch', 'post']


class DiagnosticianViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = DiagnosticianSerializer
    queryset = Diagnostician.objects.all()
    http_method_names = ['get', 'patch', 'post']


class PrescriptionItemViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = PrescriptionItemSerializer
    queryset = PrescriptionItem.objects.all()
    http_method_names = ['get', 'patch', 'post']

class ScheduleTaskViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = ScheduleTaskSerializer
    queryset = ScheduleTask.objects.all()
    http_method_names = ['get', 'patch', 'post']

class MedicineViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()
    http_method_names = ['get', 'patch', 'post']


class PrescriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()
    http_method_names = ['get', 'patch', 'post']

