from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from passlib.hash import pbkdf2_sha256
from django.db.models import Q

from . serializers import patient_signup_serializer
from . serializers import specialist_signup_serializer
from . serializers import appointment_serializer
from . serializers import medical_record_serializer
#from . serializers import comments_serializer
from . models import patient_signup
from . models import specialist_signup
from . models import appointment
from . models import Document
#from . models import comments



class hello_world(APIView):

    def get(self, request):
        
        return Response({"name": "hello world"})





class patient_sign_up(APIView):

    def get(self, request):
        data_stored = patient_signup.objects.all()
        dataserialized = patient_signup_serializer(data_stored, many = True)
        data_dict = dataserialized.data
        return Response(data_dict)
        

    def post(self, request):
        
        data_serial = patient_signup_serializer(data = request.data, many = True)
        specialist_data_check_also = specialist_signup_serializer(data = request.data, many = True)
        if data_serial.is_valid() and specialist_data_check_also.is_valid():
            data_list_of_dict = data_serial.data
            data_dict = data_list_of_dict[0]
            enc_password = pbkdf2_sha256.encrypt(data_dict['password'], rounds = 12000, salt_size = 32)

            saver = patient_signup(email = data_dict['email'],
                                   name = data_dict['name'],
                                   date = data_dict['date'],
                                   password = enc_password)
            saver.save()
            return Response({"status":"Ok"})
        else:
            if (data_serial.is_valid()==False):
                return Response({"status":data_serial.errors})
            else:
                return Response({"status":specialist_data_check_also.errors})         







class specialist_sign_up(APIView):

    def get(self, request):

        data_stored = specialist_signup.objects.all()
        dataserialized = specialist_signup_serializer(data_stored, many = True)
        data_dict = dataserialized.data
        return Response(data_dict)

    def post(self, request):

        data_serial = specialist_signup_serializer(data = request.data, many = True)
        patient_check_up_also = patient_signup_serializer(data = request.data, many = True)

        if data_serial.is_valid() and patient_check_up_also.is_valid():
            data_list_of_dict = data_serial.data
            data_dict = data_list_of_dict[0]
            enc_password = pbkdf2_sha256.encrypt(data_dict['password'], rounds = 12000, salt_size = 32)

            saver = specialist_signup(email = data_dict['email'],
                                      name = data_dict['name'],
                                      speciality = data_dict['speciality'],
                                      experience = data_dict['experience'],
                                      place_of_practice = data_dict['place_of_practice'],
                                      postal_code = data_dict['postal_code'],
                                      password = enc_password)
            saver.save()
            return Response({"status":"Ok"})
        else:
            if(data_serial.is_valid()==False):
                return Response({"status":data_serial.errors})
            else:
                return Response({"status":patient_check_up_also.errors})     








class patient_doctor_login(APIView):

    def post(self, request):
        data_serial = patient_signup_serializer(data = request.data, many = True)
        data_serial_specialist = specialist_signup_serializer(data = request.data, many = True)

        if data_serial.is_valid() and data_serial_specialist.is_valid():
            return Response({"status":"Account with this email id does not exists"})
        else:
            if(data_serial.is_valid()==False):

                data_list_of_dict = data_serial.data
                data_dict = data_list_of_dict[0]
                data_stored_object = patient_signup.objects.filter(email = data_dict["email"])
                dataserialized = patient_signup_serializer(data_stored_object, many = True)
                patient_data_dict = dataserialized.data

                password_verify = pbkdf2_sha256.verify(data_dict["password"], (patient_data_dict[0])["password"])

                if(password_verify):
                    return Response({"status": "Ok", "details" :patient_data_dict, "is_it_patient": 1})
                else:
                    return Response({"status":"Password Incorrect"})    

            else:

                data_list_of_dict = data_serial_specialist.data
                data_dict = data_list_of_dict[0]
                data_stored_object = specialist_signup.objects.filter(email = data_dict["email"])
                dataserialized = specialist_signup_serializer(data_stored_object, many = True)
                specialist_data_dict = dataserialized.data

                password_verify = pbkdf2_sha256.verify(data_dict["password"], (specialist_data_dict[0])["password"])

                if(password_verify):
                    return Response({"status": "Ok", "details": specialist_data_dict, "is_it_patient": 0})
                else:
                    return Response({"status":"Password Incorrect"})    





        
class appointments(APIView):

    def get(self, request, email_id="", patient_or_specialist=0):
        if(patient_or_specialist==0):
            appointment_data_objects = appointment.objects.filter(specialist_email_id = email_id)
            appointment_serial =  appointment_serializer(appointment_data_objects, many = True)
            appointment_data = appointment_serial.data
            return Response(appointment_data)
        else:
            appointment_data_objects = appointment.objects.filter(patient_email_id = email_id)
            appointment_serial =  appointment_serializer(appointment_data_objects, many = True)
            appointment_data = appointment_serial.data
            return Response(appointment_data)

    def post(self, request):

        data_serial = appointment_serializer(data = request.data, many = True)
        
        if(data_serial.is_valid()):
            data_appoint = data_serial.data
            data_dict = data_appoint[0]

            saver = appointment(patient_email_id = data_dict["patient_email_id"],
                                specialist_email_id = data_dict["specialist_email_id"],
                                date = data_dict["date"],
                                time_start = data_dict["time_start"],
                                time_end = data_dict["time_end"],
                                type_of_call = data_dict["type_of_call"])

            saver.save()
            return Response({"status":"Ok"})

        else:
            return Response({"status":data_serial.errors})    




class uploads(APIView):

    def get(self, request, email_user="", title_file=""):
         data_stored = Document.objects.filter(email = email_user).filter(title = title_file)
         response = HttpResponse(data_stored[0].doc_file, content_type='application/.pdf')
         response['Content-Disposition'] = 'inline;'
         return response

    def post(self, request):
        print(request.FILES['myFile'])
        print(request.data["for_patient"])
        newdoc = Document(doc_file=request.FILES.get('myFile'), title=request.FILES['myFile'], email=request.data["for_patient"])
        newdoc.save()

        return Response({"status":str(request.FILES['myFile'])})

class get_med_records(APIView):

    def get(self, request, email_id=""):
        data_stored = Document.objects.filter(email = email_id)
        data_serial = medical_record_serializer(data_stored, many = True)
        data_sto = data_serial.data
        return Response({"status":data_sto})

'''
class comment(APIView):

    def get(self, request,  sender_email="", receiver_email=""):
        data_stored = comments.objects.filter(Q(email_sender = sender_email, email_receiver = receiver_email)|Q(email_sender = receiver_email, email_receiver = sender_email))
        dataserialized = comments_serializer(data_stored, many = True)
        data_dict = dataserialized.data
        return Response(data_dict)

    def post(self, request):

        data_serial = comments_serializer(data = request.data, many = True)
        
        if(data_serial.is_valid()):
            data_appoint = data_serial.data
            data_dict = data_appoint[0]

            saver = comments(email_sender = data_dict["email_sender"],
                             email_receiver = data_dict["email_receiver"],
                             comment = data_dict["comment"]
                            )

            saver.save()
            return Response({"status":"Ok"})

        else:
            return Response({"status":data_serial.errors})    
        

#[{"email_sender":"sajal@gmail.com","email_receiver":"ss@ww.com","comment":"Hey"}]
#[{"email_receiver":"sajal@gmail.com","email_sender":"ss@ww.com","comment":"Am fine"}]

'''


# Create your views here.
