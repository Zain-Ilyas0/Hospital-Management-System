from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('doctor/', views.doctor, name="doctor"),
    path('doctorAPI/', views.DoctorListCreate.as_view(), name="doctorAPI"),
    path("view_doctor/<int:id>/", views.view_doctor, name="view_doctor"),
    path("edit_doctor/<int:id>/", views.edit_doctor, name="edit_doctor"),
    path("delete_doctor/<int:id>/", views.delete_doctor, name="delete_doctor"),
    path('patient/', views.patient, name="patient"),
    path('patientAPI/', views.PatientListCreate.as_view(), name="patientAPI"),
    path("edit_patient/<int:id>/", views.edit_patient, name="edit_patient"),
    path("delete_patient/<int:id>/", views.delete_patient, name="delete_patient"),
    path("patient_search/", views.patient_search, name="patient_search"),
    path("logout/", views.logout_view, name="logout"),


]
