from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views
# from rest_framework import routers
from clinic.views import AppointmentViewSet, DiagnosticianViewSet, \
    PrescriptionItemViewSet

router = routers.DefaultRouter()


router.register(prefix='appointment', viewset=AppointmentViewSet, basename='user')
router.register(prefix='diagnostician', viewset=DiagnosticianViewSet, basename='user')
router.register(prefix='prescription', viewset=PrescriptionItemViewSet, basename='user')

urlpatterns = [

]
