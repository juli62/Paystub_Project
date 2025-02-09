import base64
import pathlib
from django.conf import settings
from .style import css
import os

def config_paystub(company,country,full_name,email,position,health_discount_amount,social_discount_amount,taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period):
   
   languageContent =[]
   company_logo =  get_logo(company,country)
   languageES = ["Posición","Salario Bruto","Pago Bruto","Descuentos","SFS","AFP","ISR","Otros","Comprobante de Pago","Pago Neto"]
   languageEN = ["Position","Gross Salary","Gross Payment","Discounts","Health Insurance","Social Security","Taxes","Others","Paystub Payment","Net Payment"]
   if country == "USA":
        languageContent = languageEN
   elif country == "DO":
        languageContent = languageES     
   
   html =f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{languageContent[8]}</title>
        <style>
        {css}
        </style>
    </head>
    <body>
        <h2>{languageContent[8]}</h2>
        
        <div class="section">
            
            <img class="logo" src="{company_logo}" contenttype="image/png"></img>
        </div>
        <div class="section">
            <strong>{full_name}</strong><br>
            <strong>Email:</strong> {email}<br>
            <strong>{languageContent[0]}</strong> {position}
        </div>


        <table class="details">
            <tr>
                <th>{languageContent[1]}</th>
                
                <th colspan="2">{languageContent[3]}</th>
            </tr>
            <tr>
                <td>{gross_salary}</td>
            
                <td>{languageContent[4]}</td>
                <td>{health_discount_amount}</td>
            </tr>
            <tr>
                <th>{languageContent[2]}</th>
            
                <td>{languageContent[5]}</td>
                <td>{social_discount_amount}</td>
            </tr>
            <tr>
                <td>{gross_payment}</td>
            
                <td>{languageContent[6]}</td>
                <td>{taxes_discount_amount}</td>
            </tr>
            <tr>
                
                <td>-</td>
                <td>{languageContent[7]}</td>
                <td>{other_discount_amount}</td>
            </tr>
            <tr class="total">
            
            </tr>
            <tr>
                
                
                <th colspan="2">Total</th>
                <td>{social_discount_amount + health_discount_amount + taxes_discount_amount + other_discount_amount}</td>
            </tr>
            <tr class="total">
                <td colspan="2">{languageContent[9]}</td>
                <td>{net_payment}</td>
            </tr>
        </table>
        <br>
        <strong>{languageContent[8]}:</strong> {period}
    </body>
    </html>"""
   save_html(html)
   return html
    


def get_logo(company,country):
   
    company_logo = os.path.join(settings.MEDIA_ROOT, f"{company}.png")
    
    if not os.path.exists(company_logo): 
        if country == "USA":
           company_logo = os.path.join(settings.MEDIA_ROOT, f"defaultEN.png")  
        elif country == "DO":
             company_logo = os.path.join(settings.MEDIA_ROOT, f"defaultES.png")    
    with open(company_logo,"rb") as img:
        base64_string = base64.b64encode(img.read()).decode("utf-8")
    return f"data:image/png;base64,{base64_string}"


#delete later
def save_html(html_content, filename="output.html"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
   
