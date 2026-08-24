from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework import generics
from .models import Doctor, Patient
from .serializers import DoctorSerializers, PatientSerializers
from rest_framework.parsers import FormParser, MultiPartParser
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import logout



# Create your views here.

class DoctorListCreate(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializers
    parser_classes = [FormParser, MultiPartParser]


class PatientListCreate(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializers
    parser_classes = [FormParser, MultiPartParser]



def homepage(request):
    is_hospital_admin = request.user.groups.filter(
        name="Hospital Admin"
    ).exists()

    return render(request, "homepage.html", {
        "is_hospital_admin": is_hospital_admin
    })




@login_required
@user_passes_test(lambda user: user.groups.filter(name="Hospital Admin").exists())
def doctor(request):
    if request.method == "POST":
        Doctor.objects.create(
            first_name = request.POST.get('first_name'),
            last_name = request.POST.get('last_name'),
            date_of_birth = request.POST.get('date_of_birth'),
            cnic = request.POST.get('cnic'),
            gender = request.POST.get('gender'),
            phone_number = request.POST.get('phone_number'),
            email = request.POST.get('email'),
            address = request.POST.get('address'),
            specialization = request.POST.get('specialization'),
            qualification = request.POST.get('qualification'),
        )

        return redirect('doctor')

    doctors = Doctor.objects.all()
        


    return render(request, "doctor.html", {'doctors': doctors})









def view_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    return render(request, "viewdoctor.html", {
        "doctor": doctor
    })


@login_required
@user_passes_test(lambda user: user.groups.filter(name="Hospital Admin").exists())
def edit_doctor(request, id):


    doctor = get_object_or_404(Doctor, id=id)


    if request.method == "POST":
            
        doctor.first_name = request.POST.get('first_name')
        doctor.last_name = request.POST.get('last_name')
        doctor.date_of_birth = request.POST.get('date_of_birth')
        doctor.cnic = request.POST.get('cnic')
        doctor.gender = request.POST.get('gender')
        doctor.phone_number = request.POST.get('phone_number')
        doctor.email = request.POST.get('email')
        doctor.address = request.POST.get('address')
        doctor.specialization = request.POST.get('specialization')
        doctor.qualification = request.POST.get('qualification')

        doctor.save()

        return redirect("doctor")

    doctors = Doctor.objects.all()

    return render(request, "doctor.html", {
        "doctors": doctors,
        "edit_doctor": doctor
    })


@login_required
@user_passes_test(lambda user: user.groups.filter(name="Hospital Admin").exists())
def delete_doctor(request, id):

    doctor = get_object_or_404(Doctor, id=id)

    doctor.delete()

    return redirect("doctor")



@login_required
def patient(request):

    is_admin = request.user.groups.filter(
        name="Hospital Admin"
    ).exists()

    is_doctor = request.user.groups.filter(
        name="Doctor"
    ).exists()

    is_receptionist = request.user.groups.filter(
        name="Receptionist"
    ).exists()

    if is_admin:

        if request.method == "POST":

            doctor_id = request.POST.get("doctor")

            doctor = Doctor.objects.filter(
                id=doctor_id
            ).first()

            if doctor is None:

                return render(request, "patient.html", {
                    "patients": Patient.objects.all(),
                    "doctors": Doctor.objects.all(),

                    "is_admin": True,
                    "is_doctor": False,
                    "is_receptionist": False,

                    "error": "Please select a valid doctor."
                })

            Patient.objects.create(
                patient_name=request.POST.get("patient_name"),
                age=request.POST.get("age"),
                gender=request.POST.get("gender"),
                phone_number=request.POST.get("phone_number"),
                patient_problem=request.POST.get("patient_problem"),
                doctor=doctor
            )

            return redirect("patient")

        patients = Patient.objects.all()

        doctors = Doctor.objects.all()


        return render(request, "patient.html", {

            "patients": patients,
            "doctors": doctors,

            "is_admin": True,
            "is_doctor": False,
            "is_receptionist": False,
        })


    if is_receptionist:

        if request.method == "POST":

            doctor_id = request.POST.get("doctor")

            doctor = Doctor.objects.filter(
                id=doctor_id
            ).first()
            if doctor is None:

                return render(request, "patient.html", {
                    "patients": Patient.objects.all(),
                    "doctors": Doctor.objects.all(),

                    "is_admin": False,
                    "is_doctor": False,
                    "is_receptionist": True,

                    "error": "Please select a valid doctor."
                })


            Patient.objects.create(
                patient_name=request.POST.get("patient_name"),
                age=request.POST.get("age"),
                gender=request.POST.get("gender"),
                phone_number=request.POST.get("phone_number"),
                patient_problem=request.POST.get("patient_problem"),
                doctor=doctor
            )

            return redirect("patient")


        patients = Patient.objects.all()

        doctors = Doctor.objects.all()


        return render(request, "patient.html", {

            "patients": patients,
            "doctors": doctors,

            "is_admin": False,
            "is_doctor": False,
            "is_receptionist": True,
        })


    if is_doctor:

        doctor = Doctor.objects.filter(
            user=request.user
        ).first()


        if doctor is None:

            return render(request, "patient.html", {

                "patients": [],
                "doctors": [],

                "is_admin": False,
                "is_doctor": True,
                "is_receptionist": False,

                "error": "No Doctor record is linked to this user."
            })

        if request.method == "POST":

            Patient.objects.create(
                patient_name=request.POST.get("patient_name"),
                age=request.POST.get("age"),
                gender=request.POST.get("gender"),
                phone_number=request.POST.get("phone_number"),
                patient_problem=request.POST.get("patient_problem"),
                doctor=doctor
            )

            return redirect("patient")

        patients = Patient.objects.filter(
            doctor=doctor
        )
        return render(request, "patient.html", {

            "patients": patients,

            # Doctor does not need
            # doctor dropdown
            "doctors": [],

            "is_admin": False,
            "is_doctor": True,
            "is_receptionist": False,
        })

    return redirect("homepage")
@login_required
def edit_patient(request, id):

    patient = get_object_or_404(Patient, id=id)

    is_admin = request.user.groups.filter(
        name="Hospital Admin"
    ).exists()

    is_doctor = request.user.groups.filter(
        name="Doctor"
    ).exists()

    is_receptionist = request.user.groups.filter(
        name="Receptionist"
    ).exists()

    # -----------------------------
    # DETERMINE ROLE (mutually exclusive, admin takes priority)
    # -----------------------------

    if is_admin:
        role = "admin"
    elif is_receptionist:
        role = "receptionist"
    elif is_doctor:
        role = "doctor"
    else:
        return redirect("patient")

    # -----------------------------
    # DOCTOR PERMISSION
    # -----------------------------

    current_doctor = None

    if role == "doctor":

        current_doctor = Doctor.objects.filter(
            user=request.user
        ).first()

        if current_doctor is None:
            return redirect("patient")

        # Doctor can edit only his own patient
        if patient.doctor != current_doctor:
            return redirect("patient")

    # -----------------------------
    # POST - UPDATE PATIENT
    # -----------------------------

    if request.method == "POST":

        patient.patient_name = request.POST.get("patient_name")
        patient.age = request.POST.get("age")
        patient.gender = request.POST.get("gender")
        patient.phone_number = request.POST.get("phone_number")
        patient.patient_problem = request.POST.get("patient_problem")

        # Admin and Receptionist can change doctor
        if role in ("admin", "receptionist"):

            doctor_id = request.POST.get("doctor")

            if not doctor_id:
                return render(request, "patient.html", {
                    "patients": Patient.objects.all(),
                    "doctors": Doctor.objects.all(),
                    "edit_patient": patient,
                    "is_admin": is_admin,
                    "is_doctor": is_doctor,
                    "is_receptionist": is_receptionist,
                    "error": "Please select a doctor."
                })

            doctor = get_object_or_404(
                Doctor,
                id=doctor_id
            )

            patient.doctor = doctor

        # Doctor stays assigned to himself
        else:  # role == "doctor"

            patient.doctor = current_doctor

        patient.save()

        return redirect("patient")

    # -----------------------------
    # GET - SHOW EDIT FORM
    # -----------------------------

    if role in ("admin", "receptionist"):

        patients = Patient.objects.all()
        doctors = Doctor.objects.all()

    else:  # role == "doctor"

        patients = Patient.objects.filter(
            doctor=current_doctor
        )

        doctors = Doctor.objects.filter(
            id=current_doctor.id
        )

    return render(request, "patient.html", {
        "patients": patients,
        "doctors": doctors,
        "edit_patient": patient,
        "is_admin": is_admin,
        "is_doctor": is_doctor,
        "is_receptionist": is_receptionist,
    })







@login_required
def delete_patient(request, id):

    # Get the patient
    patient = get_object_or_404(Patient, id=id)

    # Check roles
    is_admin = request.user.groups.filter(
        name="Hospital Admin"
    ).exists()

    is_doctor = request.user.groups.filter(
        name="Doctor"
    ).exists()

    is_receptionist = request.user.groups.filter(
        name="Receptionist"
    ).exists()

    # -----------------------------
    # ADMIN AND RECEPTIONIST
    # Can delete ANY patient
    # -----------------------------
    if is_admin or is_receptionist:

        patient.delete()
        return redirect("patient")

    # -----------------------------
    # DOCTOR
    # Can delete ONLY own patients
    # -----------------------------
    if is_doctor:

        current_doctor = Doctor.objects.filter(
            user=request.user
        ).first()

        # Doctor account is not linked to Doctor record
        if current_doctor is None:
            return redirect("patient")

        # Doctor cannot delete another doctor's patient
        if patient.doctor != current_doctor:
            return redirect("patient")

        patient.delete()
        return redirect("patient")

    # -----------------------------
    # OTHER USERS NOT ALLOWED
    # -----------------------------
    return redirect("patient")







def login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            if user.groups.filter(name="Hospital Admin").exists():
                return redirect("homepage")

            elif user.groups.filter(name="Doctor").exists():
                return redirect("patient")

            elif user.groups.filter(name="Receptionist").exists():
                return redirect("patient")

            else:
                return render(request, "login.html", {
                    "error": "Your account has no assigned role."
                })

        else:
            return render(request, "login.html", {
                "error": "Wrong username or password."
            })

    return render(request, "login.html")







def register(request):

    if request.method == "POST":

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "register.html", {
                "error": "Passwords do not match."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {
                "error": "Username already exists."
            })

        User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        return redirect("login")

    return render(request, "register.html")






# def patient_search(request):
#     patient = None
#     error = None

#     if request.method == "POST":
#         patient_id = request.POST.get("patient_id")
#         patient_name = request.POST.get("patient_name")

#         try:
#             patient = Patient.objects.get(
#                 id=patient_id,
#                 patient_name__iexact=patient_name.strip()
#             )
#         except Patient.DoesNotExist:
#             error = "No patient found with this ID and name."

#     return render(request, "patientsearch.html", {
#         "patient": patient,
#         "error": error
#     })


def patient_search(request):
    patient = None
    error = None
    patient_number = None

    patients = list(
        Patient.objects.select_related("doctor").all()
    )

    if request.method == "POST":

        patient_number = request.POST.get("patient_id")
        patient_name = request.POST.get("patient_name", "").strip()

        try:
            number = int(patient_number)

            if number < 1 or number > len(patients):
                error = "Patient ID does not exist."

            else:
                # forloop.counter starts at 1
                patient = patients[number - 1]

                # Compare names
                if patient.patient_name.strip().lower() != patient_name.lower():
                    patient = None
                    error = "Patient ID and Patient Name do not match."

        except (ValueError, TypeError):
            error = "Please enter a valid Patient ID."

    return render(request, "patientsearch.html", {
        "patient": patient,
        "error": error,
        "patient_number": patient_number,
    })



def logout_view(request):
    logout(request)
    return redirect("homepage")