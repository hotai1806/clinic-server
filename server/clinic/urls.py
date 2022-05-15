from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
# from rest_framework import routers
from clinic.views import AppointmentViewSet, DiagnosticianViewSet, \
    PrescriptionItemViewSet, PrescriptionViewSet, ScheduleTaskViewSet, \
    MedicineViewSet, get_history_appointment

router = routers.DefaultRouter()


router.register(prefix='appointment', viewset=AppointmentViewSet, basename='user')
router.register(prefix='diagnostician', viewset=DiagnosticianViewSet, basename='user')
router.register(prefix='prescription-detail', viewset=PrescriptionItemViewSet, basename='user')
router.register(prefix='prescription', viewset=PrescriptionViewSet, basename='user')
router.register(prefix='schedule-task', viewset=ScheduleTaskViewSet, basename='user')
router.register(prefix='medicine', viewset=MedicineViewSet, basename='user')
urlpatterns = [
    path('appointment-history/<int:pk>/', get_history_appointment),

]
