from this import s
from urllib import response
from django.shortcuts import render
from rest_framework import viewsets, status, permissions, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q, Sum, Count
from authentication.models import User

from django.core import serializers

from clinic.serializers import PaymentSerializer

from .models import Appointment, Diagnostician, Payment,\
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
from server.perm import CustomDjangoModelPermission



class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.IsAuthenticated)]
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    http_method_names = ['get', 'patch', 'post']

    def create(self, request, *args, **kwargs):
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
            get_current_docter = User.objects.get(id=request.data['user_id'] if 'user_id' in request.data else '1')
            get_current_approve_user = User.objects.get(id=request.data['user_approve_id'] if 'user_approve_id' in request.data else '1')
            data_copy = request.data.copy()
            print("double check", get_current_account_id)
            data_copy['patient_id'] = str(get_current_account_id)
            data_copy['user_id'] = str(get_current_docter.id)
            data_copy['user_approve_id'] = str(get_current_approve_user.id)

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

    def list(self, request, *args, **kwargs):
        try:
            get_current_account_id = request.META['current_account_id']
            user_current = User.objects.get(
                id=get_current_account_id).groups.values_list('name', flat=True)
            if 'staff' in user_current or 'nurse' in user_current or \
                    'doctor' in user_current or 'admin' in user_current:
                return super().list(request, *args, **kwargs)
            self.queryset = self.queryset.filter(
                patient_id=get_current_account_id)
            return super().list(request, *args, **kwargs)
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
    queryset = ScheduleTask.objects.all().order_by('-appointment_date')
    http_method_names = ['get', 'patch', 'post']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']


class MedicineViewSet(viewsets.ModelViewSet):
    permission_classes = [(CustomDjangoModelPermission)]
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()
    http_method_names = ['get', 'patch', 'post']
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']


class PaymentVietSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    http_method_names = ['get', 'patch', 'post']


class PrescriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [(permissions.AllowAny)]
    serializer_class = PrescriptionSerializer
    queryset = Prescription.objects.all().order_by('id')
    http_method_names = ['get', 'patch', 'post']

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            list_items = data.pop('list_items')
            prescription = Prescription.objects.create(
                patient_id=request.data['patient_id'],
                total_amount=request.data.get('total_amount', 0),
            )
            prescription.save()
            for item in list(list_items):
                PrescriptionItem.objects.create(
                    prescription_id=prescription.id,
                    medicine_id=int(item['medicine_id']),
                    quantity=int(item['quantity']),
                    description=item.get('description', ''),
                )
            return Response(data={"prescription_id": prescription.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("main", e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


@ api_view(['GET'])
@ permission_classes((permissions.AllowAny,))
def get_history_appointment(request):
    try:
        query_appointment_date = request.GET.get('appointment_date')
        query_patient_id = request.GET.get('patient_id')
        get_history_appointment = Appointment.objects.order_by(
            '-appointment_date').all()
        if query_patient_id:
            get_history_appointment = get_history_appointment.filter(
                patient_id=query_patient_id)
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


@api_view(['GET'])
@authentication_classes([])
@permission_classes((permissions.AllowAny, ))
def static_payment(request):
    from django.db import connection
    filter_query = request.GET.get('filter_query')

    truncate_month = connection.ops.date_trunc_sql('month', 'created_date')
    payment = Payment.objects.extra({'month': truncate_month}).values(
        'created_date__month').annotate(Sum('total_amount')).distinct()
    return Response(data=payment)


@api_view(['GET'])
@authentication_classes([])
@permission_classes((permissions.AllowAny, ))
def static_patient(request):
    from django.db import connection

    truncate_month = connection.ops.date_trunc_sql('month', 'created_date')
    patient = Appointment.objects.extra({'month': truncate_month}).values(
        'created_date__month').annotate(Count('patient_id')).distinct()

    return Response(data=patient)
