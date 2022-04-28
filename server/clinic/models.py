from django.db import models
from authentication.models import ModelBase, User
# Create your models here.

class ScheduleTask(ModelBase):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()


class Appointment(ModelBase):
    user = models.ForeignKey(User,null=False,related_name='user', on_delete=models.CASCADE)
    patient = models.ForeignKey(User,null=False,related_name='patient' , on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()

class Medicine(ModelBase):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
class Prescription(ModelBase):
    patient = models.ForeignKey(User,null=False, on_delete=models.CASCADE)
    total_amount = models.FloatField()


class PrescriptionItem(ModelBase):
    prescription = models.ForeignKey(Prescription,null=False, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField()

