from rest_framework import serializers
from clinic.models import Appointment, Medicine, \
    Prescription, PrescriptionItem, ScheduleTask, Diagnostician\
        ,Payment
from authentication.models import User
from authentication.serializers import UserSerializer


class AppointmentSerializer(serializers.ModelSerializer):
    '''
    Create Diagnosise include data{
    }
    '''
    patient_id = serializers.CharField(max_length=255)
    user_id = serializers.CharField(max_length=255)
    user_approve_id = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=255, allow_blank=True)

    class Meta:
        model = Appointment
        fields = ["id", "patient_id",
                  "user_id", "appointment_date",
                  "user_approve_id", "status"]
        read_only = ['id']


class DiagnosticianSerializer(serializers.ModelSerializer):
    '''
    Create Diagnosise include data{
    }
    '''
    patient_id = serializers.CharField(max_length=255)

    class Meta:
        model = Diagnostician
        fields = ["id", 'patient_id', "patient", "symptom",
                  "conclusion", ]
        read_only = ["id", "patient"]
        depth = 1


class PrescriptionItemSerializer(serializers.ModelSerializer):
    '''
    Create Diagnosise include data{
    }
    '''
    prescription_id = serializers.CharField(max_length=255)
    medicine_id = serializers.CharField(max_length=255)

    class Meta:
        model = PrescriptionItem
        fields = ["id", "quantity", "medicine",
                  "medicine_id", 'prescription_id']
        read_only = ['id']
        extra_kwargs = {
            'url': {'lookup_field': 'prescription_id'},
        }
        depth = 1


class ScheduleTaskSerializer(serializers.ModelSerializer):
    '''
    Create ScheduleTask include data{
    }
    '''
    user_id = serializers.CharField(max_length=255)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ScheduleTask
        fields = ["id", "user_id", "user", "appointment_date"]
        read_only = ['id', "user"]
        depth = 1


class MedicineSerializer(serializers.ModelSerializer):
    '''
    Create Medicine include data{
    }
    '''
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    price = serializers.CharField(max_length=255)

    class Meta:
        model = Medicine
        fields = ["id", "name", "description", "price"]
        read_only = ['id']
        depth = 1


class PrescriptionSerializer(serializers.ModelSerializer):
    '''
    Create Prescription include data{
    }
    '''
    patient_id = serializers.CharField(max_length=255)
    patient = UserSerializer(read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = ["id", "patient_id", "patient",
                  "total_amount", "items",]
        read_only = ['id']
        depth = 2
    # def create(self, validated_data):
    #     return super().create(validated_data)

class PaymentSerializer(serializers.ModelSerializer):
    '''
    Create Payment include data{
    }
    '''
    patient_id = serializers.CharField(max_length=255)
    doctor_id = serializers.CharField(max_length=255)
    prescription_id = serializers.CharField(max_length=255)

    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    medical_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    # Field Views
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "patient_id", "patient", "medical_cost",
                  "doctor_id", "total_amount","prescription_id","created_date"]
        read_only = ['id']
        depth = 2
    # def create(self, validated_data):
    #     return super().create(validated_data)