from rest_framework import serializers
from clinic.models import Appointment, Medicine, \
    Prescription, PrescriptionItem, ScheduleTask, Diagnostician


class AppointmentSerializer(serializers.ModelSerializer):
    '''
    Create Diagnosise include data{
    }
    '''
    patient_id = serializers.CharField(max_length=255)
    user_id = serializers.CharField(max_length=255)

    class Meta:
        model = Appointment
        fields = ["id", "patient_id",
                  "user_id", "appointment_date"]
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
        fields = ["id", "quantity",
                  "medicine_id", 'prescription', 'prescription_id']
        read_only = ['id']
        depth = 1


class ScheduleTaskSerializer(serializers.ModelSerializer):
    '''
    Create ScheduleTask include data{
    }
    '''
    user_id = serializers.CharField(max_length=255)

    class Meta:
        model = ScheduleTask
        fields = ["id", "user_id", "user", "appointment_date"]
        read_only = ['id', "user"]
        depth = 1


class PrescriptionSerializer(serializers.ModelSerializer):
    '''
    Create Prescription include data{
    }
    '''
    patient_id = serializers.CharField(max_length=255)

    class Meta:
        model = Prescription
        fields = ["id", "patient_id", "patient", "total_amount"]
        read_only = ['id', "user"]
        depth = 1


class MedicineSerializer(serializers.ModelSerializer):
    '''
    Create Medicine include data{
    }
    '''

    class Meta:
        model = Medicine
        fields = ["id", "name", "description", "price"]
        read_only = ['id']
        depth = 1