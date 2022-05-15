from django.contrib import admin
from clinic.models import (Appointment, Medicine,
                           Prescription, PrescriptionItem, ScheduleTask,
                           Diagnostician)

# Register your models here.
admin.site.register(Appointment)
admin.site.register(Medicine)
admin.site.register(Prescription)
admin.site.register(PrescriptionItem)
admin.site.register(ScheduleTask)
admin.site.register(Diagnostician)

