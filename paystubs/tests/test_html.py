import base64
import pytest
from unittest.mock import patch

from django.conf import settings


from api.paystub import config_paystub, get_logo

@pytest.mark.django_db
def test_config_paystub_english(tmp_path):
    
    
    company = "AtDev"
    country = "USA"
    full_name = "Juan Manuel"
    email = "juanmanuel14@gmail.com"
    position = "Web Developer"
    health_discount_amount = 50
    social_discount_amount = 25
    taxes_discount_amount = 100
    other_discount_amount = 0
    gross_salary = 2000
    gross_payment = 1800
    net_payment = 1625
    period = "2025-02-15"

    
    html_content = config_paystub(
        company=company,
        country=country,
        full_name=full_name,
        email=email,
        position=position,
        health_discount_amount=health_discount_amount,
        social_discount_amount=social_discount_amount,
        taxes_discount_amount=taxes_discount_amount,
        other_discount_amount=other_discount_amount,
        gross_salary=gross_salary,
        gross_payment=gross_payment,
        net_payment=net_payment,
        period=period
    )

    
    assert "Position" in html_content
    assert "Gross Salary" in html_content
    assert "Gross Payment" in html_content
    assert "Discounts" in html_content
    assert "Health Insurance" in html_content
    assert "Social Security" in html_content
    assert "Taxes" in html_content
    assert "Others" in html_content
    assert "Paystub Payment" in html_content
    assert "Net Payment" in html_content
    assert str(gross_salary) in html_content
    assert str(net_payment) in html_content
    assert period in html_content


@pytest.mark.django_db
def test_config_paystub_spanish(tmp_path):
    
    
    company = "At Dev"
    country = "DO"
    full_name = "Juan Perez"
    email = "juanpi14@gmail.com"
    position = "Web Developer"
    health_discount_amount = 100
    social_discount_amount = 50
    taxes_discount_amount = 200
    other_discount_amount = 10
    gross_salary = 3000
    gross_payment = 2500
    net_payment = 2140
    period = "2025-02-15"

    
    html_content = config_paystub(
        company=company,
        country=country,
        full_name=full_name,
        email=email,
        position=position,
        health_discount_amount=health_discount_amount,
        social_discount_amount=social_discount_amount,
        taxes_discount_amount=taxes_discount_amount,
        other_discount_amount=other_discount_amount,
        gross_salary=gross_salary,
        gross_payment=gross_payment,
        net_payment=net_payment,
        period=period
    )

    
    assert "Posición" in html_content
    assert "Salario Bruto" in html_content
    assert "Pago Bruto" in html_content
    assert "Descuentos" in html_content
    assert "SFS" in html_content
    assert "AFP" in html_content
    assert "ISR" in html_content
    assert "Otros" in html_content
    assert "Comprobante de Pago" in html_content
    assert "Pago Neto" in html_content
    assert str(gross_salary) in html_content
    assert str(net_payment) in html_content
    assert period in html_content


@pytest.mark.django_db
def test_get_logo_existing_file(tmp_path):
    
    
    fake_png = tmp_path / "Facebook.png"
    with open(fake_png, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")  

    
    with patch.object(settings, 'MEDIA_ROOT', str(tmp_path)):
        
        result = get_logo("Facebook", country="USA")

   
    assert result.startswith("data:image/png;base64,")
    encoded = result.split(",")[1]
    decoded = base64.b64decode(encoded)
    assert decoded.startswith(b"\x89PNG"), "Decoded should start with PNG signature."


@pytest.mark.django_db
def test_get_logo_default_file(tmp_path):
   
    #
    default_en_logo = tmp_path / "defaultEN.png"
    with open(default_en_logo, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")

 
    with patch.object(settings, 'MEDIA_ROOT', str(tmp_path)):
       
        result = get_logo("Facebook", country="USA")

    assert result.startswith("data:image/png;base64,")
    encoded = result.split(",")[1]
    decoded = base64.b64decode(encoded)
    assert decoded.startswith(b"\x89PNG")


