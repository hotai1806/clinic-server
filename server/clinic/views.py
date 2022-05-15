from this import s
from urllib import response
from django.shortcuts import render
from rest_framework import viewsets, status, permissions, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django_filters.rest_framework import DjangoFilterBackend

from authentication.models import User

from django.core import serializers

from .models import Appointment, Diagnostician,\
    PrescriptionItem, Medicine, Prescription, ScheduleTask
from clinic.serializers import AppointmentSerializer, DiagnosticianSerializer,\
    PrescriptionItemSerializer, MedicineSerializer, PrescriptionSerializer, ScheduleTaskSerializer
# MAIL CHIMPAPI

from server.settings import MAIL_API_KEY
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
from oauth2_provider.models import AccessToken
import json

# Create your views here.


class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.IsAuthenticated)]
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    http_method_names = ['get', 'patch', 'post']

    def create(self, request,pk, *args, **kwargs):
        from datetime import datetime, timedelta
        try:
            get_current_account_id = request.META['current_account_id']
            start_date = datetime.strptime(
                request.data['appointment_date'], '%Y-%m-%dT%H:%M').date()
            end_date = start_date + timedelta(days=2)
            get_total_patient_at_date = Appointment.objects.filter(
                appointment_date__gt=start_date, appointment_date__lt=end_date).count()
            if get_total_patient_at_date >= 100:
                return Response(data={"error": "Appointment is full"}, status=status.HTTP_400_BAD_REQUEST)
            get_current_patient = User.objects.get(
                id=get_current_account_id)
            get_current_docter = User.objects.get(id=request.data['user_id'])
            # get_current_approve_user = User.objects.get(id=request.data['user_approve_id'])
            data_copy = request.data.copy()
            data_copy['patient_id'] = str(get_current_account_id)

            serializer = self.get_serializer(data=data_copy)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            #     print("API Response", response)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ApiClientError as error:
            print("mail error", error)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("main", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


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
    filterset_fields = ['name']


class PrescriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all()
    http_method_names = ['get', 'patch', 'post']


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_history_appointment(request, pk):
    try:
        query_appointment_date = request.GET.get('appointment_date')
        print(pk)
        get_history_appointment = Appointment.objects.filter(
            patient_id=pk)\
            .order_by('-appointment_date').all()
        if query_appointment_date:
            get_history_appointment = get_history_appointment.filter(
                appointment_date__date=query_appointment_date)
        print(get_history_appointment[1].appointment_date)
        # if query_appointment_date:
            # get_history_appointment.filter(appointment_date=query_appointment_date)
        serializer = serializers.serialize('json', get_history_appointment)
        return Response(data=json.loads(serializer), status=status.HTTP_200_OK)
    except Exception as e:
        print("main", e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
