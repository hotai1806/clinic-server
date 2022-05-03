from rest_framework import serializers
from clinic.models import Appointment, Medicine, \
    Prescription, PrescriptionItem, ScheduleTask,Diagnostician


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
    treatment_id = serializers.CharField(max_length=255)

    class Meta:
        model = Diagnostician
        fields = ["id", 'patient_id', "patient", "symptom",
                  'treatment_id', "treatment", 'created_at', 'updated_at']
        read_only = ['id']
        depth = 1


class PrescriptionItemSerializer(serializers.ModelSerializer):
    '''
    Create Diagnosise include data{
    }
    '''
    payment_id = serializers.CharField(max_length=255)
    drug_id = serializers.CharField(max_length=255)
    diagnostician_id = serializers.CharField(max_length=255)
    diagnostician = DiagnosticianSerializer(read_only=True)

    class Meta:
        model = PrescriptionItem
        fields = ["id", "quanlity", "payment_id",
                  "drug_id", 'diagnostician', 'diagnostician_id']
        read_only = ['id']
        depth = 1
