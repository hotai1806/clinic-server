from enum import Enum
from django.db import models
from authentication.models import ModelBase, User
# Create your models here.
class AppointmentStatus(Enum):   # A subclass of Enum
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"

class ScheduleTask(ModelBase):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()


class Appointment(ModelBase):
    user = models.ForeignKey(User,null=False,related_name='user', on_delete=models.CASCADE)
    patient = models.ForeignKey(User,null=False,related_name='patient' , on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    user_approve = models.ForeignKey(User,null=False,related_name='user_approve', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=[(tag.name, tag.value) for tag in AppointmentStatus])

class Medicine(ModelBase):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
class Prescription(ModelBase):
    patient = models.ForeignKey(User,null=False, on_delete=models.CASCADE)
    total_amount = models.FloatField()


class PrescriptionItem(ModelBase):
    prescription = models.ForeignKey(Prescription,null=False, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine,null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    description = models.TextField(null=True, blank=True)


class Diagnostician(models.Model):
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='patient_diagnostician', related_query_name='diagnostician')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    symptom = models.TextField(null=True, blank=True)
    conclusion = models.TextField(null=True, blank=True)