from pdf2image import convert_from_path
from util import preprocess_image
import pytesseract
import os
from pathlib import Path
from dotenv import load_dotenv

from parser_prescription import PrescriptionParser
from parser_patient_details import PatientDetailParser

load_dotenv()

tesseract_path = os.getenv('TESSERACT_PATH')

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract(file_path, file_format, poppler_path):
    pages = convert_from_path(file_path,poppler_path=poppler_path)
    document_text = ''

    for page in pages:
        processed_image = preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang = 'eng')
        document_text += '\n' + text

    extracted_data = None

    if file_format == 'prescription':
        extracted_data = PrescriptionParser(document_text).parse()
    elif file_format == 'patient_details':
        extracted_data = PatientDetailParser(document_text).parse()
    else:
        raise Exception(f"Document Format Not Suppourted: {file_format}")

    return extracted_data