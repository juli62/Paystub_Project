import csv
from django.core.mail import EmailMessage
from django.http import JsonResponse
import pdfkit
import pandas as pd
from weasyprint import HTML
from .paystub import config_paystub
from datetime import datetime




def create_paystub(html):
    
    pdf_bytes = HTML(string=html).write_pdf()
    return pdf_bytes

def generate_paystub(csv_file,country,company):
    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()  
    data = df.to_dict('records')
    
    for paystub in data:
        
        html = config_paystub(company,country,paystub["full_name"],paystub["email"],paystub["position"],paystub['health_discount_amount'],
                               paystub['social_discount_amount'],paystub["taxes_discount_amount"],paystub["other_discount_amount"],paystub["gross_salary"],
                               paystub["gross_payment"],paystub["net_payment"],paystub["period"])
        
        
    csv_pdf =  create_paystub(html)
    send_email(paystub["email"], csv_pdf, paystub["period"],country)
    return csv_pdf

def send_email(email, pdf, date,country):
    
    if country =="USA":
        subject = f"Payment for {date}"
        body = f"Your payment invoice for {date}"
    elif country == "DO":   
        subject = f"Pago de {date}"
        body = f"Factura de pago de {date}"
    
    from_email = "paystubjulianatdev@gmail.com"  
    recipient_list = [email]

    email_message = EmailMessage(subject, body, from_email, recipient_list)
    email_message.attach(filename=f"paystub_{date}.pdf", content=pdf, mimetype="application/pdf")

    email_message.send()
    json_response = {"Success!":f"Email sent succesfully to{email} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}
    print(json_response)
    return JsonResponse(json_response,status=200)