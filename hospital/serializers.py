from rest_framework import serializers
from . models import  Doctor
from . models import Patient


class DoctorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "first_name", "last_name", "date_of_birth", "cnic", "gender", "phone_number", "email", "address", "specialization", "qualification"]


class PatientSerializers(serializers.ModelSerializer):
    class  Meta:
        model = Patient
        fields  = ["id", "patient_name", "doctor", "age", "gender", "phone_number", "patient_problem"]
    