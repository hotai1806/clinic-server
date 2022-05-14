from urllib import response
from django.shortcuts import render
from rest_framework import viewsets, status, permissions, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django_filters.rest_framework import DjangoFilterBackend

from authentication.models import User

from .models import Appointment, Diagnostician,\
    PrescriptionItem, Medicine, Prescription, ScheduleTask
from clinic.serializers import AppointmentSerializer, DiagnosticianSerializer,\
    PrescriptionItemSerializer, MedicineSerializer, PrescriptionSerializer, ScheduleTaskSerializer
# MAIL CHIMPAPI

from server.settings import MAIL_API_KEY
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError


# Create your views here.


class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    http_method_names = ['get', 'patch', 'post']

    def create(self, request, *args, **kwargs):
        from datetime import datetime, timedelta
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            start_date = datetime.strptime(
                request.data['appointment_date'], '%Y-%m-%dT%H:%M').date()
            end_date = start_date + timedelta(days=2)
            get_total_patient_at_date = Appointment.objects.filter(
                appointment_date__gt=start_date, appointment_date__lt=end_date).count()
            

            if get_total_patient_at_date >= 100:
                return Response(data={"error": "Appointment is full"}, status=status.HTTP_400_BAD_REQUEST)
            print("serializer.validated_data", serializer.validated_data)
            get_current_patient = User.objects.get(
                id=request.data['patient_id'])
            get_current_docter = User.objects.get(id=request.data['user_id'])
            # get_current_approve_user = User.objects.get(id=request.data['user_approve_id'])

            mailchimp = MailchimpTransactional.Client(MAIL_API_KEY)
            message = {
                "from_email": "clinic@mailchimp.com",
                "subject": "Appointment",
                "text": "You have an appointment with Dr. {} at {}"
                .format(get_current_docter.first_name,
                        request.data.get('appointment_date')),
                "to": [
                    {
                        "email": get_current_patient.username,
                        "type": "to"
                    }
                ]
            }
            # response = mailchimp.messages.send(message)
            # if response.status_code == 200:
            serializer.save()

            #     print("API Response", response)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ApiClientError as error:
            print("mail error", error)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("main", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['^name']


class PrescriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()
    http_method_names = ['get', 'patch', 'post']
