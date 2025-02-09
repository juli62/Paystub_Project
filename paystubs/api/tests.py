from django.test import TestCase
import unittest
from unittest.mock import patch
from weasyprint import HTML
from .serializers import create_paystub
# Create your tests here.


class createPaystubTest(unittest.TestCase):

    @patch("weasyprint.HTML.write_pdf")
    def create_paystub_test(self, test_pdf):
        test_pdf.return_value=
