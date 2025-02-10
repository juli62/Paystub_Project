from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
import json
import csv
import os
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from .serializers import generate_paystub, send_email, succesful_emails_sent
from os import environ
from datetime import datetime
load_dotenv()


USER_NAME = os.getenv("USER_NAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")
# Create your views here.
@csrf_exempt
def csv_request(request):
    if request.method == 'POST':
        try:
            country = request.GET.get('country','DO')
            credentials = request.GET.get('credentials','')
            company = request.GET.get('company','')

            if country not in ["DO","USA"]:
                return JsonResponse({"Error":"Bad Request...Invalid Country"},status=400)
            
            if ' ' in credentials:
                username,password = credentials.split(' ',1)
            else:
                return JsonResponse({"Error": "Bad Request...Invalid credential format"},status=400)    
            if username != USER_NAME or password != USER_PASSWORD:
                return JsonResponse({"Error":"Invalid Credentials!"},status=400)
            if not company:
                return JsonResponse({"Error": "Bad Request...Missing Company"},status = 400)
            
            if 'file' not in request.FILES:
                return JsonResponse({"Error": "Bad Request...No CSV Uploaded"}, status=400)
            
            uploaded_csv = request.FILES['file']
            pdf_bytes = generate_paystub(uploaded_csv,country,company)
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="paystub.pdf"'
            
            #Saves the JSON response with the Emails it's been sent to
            json_response = {"Success!":f"Emails sent succesfully to {succesful_emails_sent} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
            
            #Empties the array for future batches
            for elements in succesful_emails_sent:
                succesful_emails_sent.remove(elements)
            return JsonResponse(json_response,status=200)

        except Exception as e:
            return JsonResponse({"Error": str(e)}, status=500)
        


    return JsonResponse({"Error":"Invalid request"},status=400)