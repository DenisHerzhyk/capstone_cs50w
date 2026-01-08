from celery import shared_task
from fpdf import FPDF 
import os
from django.conf import settings

@shared_task
def convert_images_to_pdf_task(file_paths):
    pdf = FPDF()
    pdf.set_auto_page_break(0) 

    for file_path in file_paths:
        pdf.add_page()
        pdf.image(file_path, x=10, y=10, w=190)

    pdf_output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'output.pdf')
    os.makedirs(os.path.dirname(pdf_output_path), exist_ok=True)
    pdf.output(pdf_output_path)
    return pdf_output_path