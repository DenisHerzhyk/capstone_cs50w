from celery import shared_task
from fpdf import FPDF 
import os
from django.conf import settings
from PIL import Image
from .models import File
import uuid

ALLOWED_EXTENSIONS = ['tiff', 'tif', 'pdf', 'png']

@shared_task
def convert_images_to_pdf_task(file_paths):
    file_paths = [f for f in file_paths if f.lower().split(".")[-1] in ALLOWED_EXTENSIONS]
    
    pdf = FPDF()
    pdf.set_auto_page_break(0) 

    for file_path in file_paths:
        pdf.add_page()
        pdf.image(file_path, x=10, y=10, w=190)

    filename = f"{uuid.uuid4()}.pdf"
    pdf_output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)
    os.makedirs(os.path.dirname(pdf_output_path), exist_ok=True)
    pdf.output(pdf_output_path)
    File.objects.create(content_type="application/pdf", file_type="extracted", file_format=pdf_output_path.split('.')[-1], file_name=filename, file_location=pdf_output_path)

    return pdf_output_path
    

@shared_task
def convert_images_to_tiff_task(file_paths):
    convert_to_tiff(file_paths, os.path.join(settings.MEDIA_ROOT, 'tiffs', 'output.tiff'))

@shared_task
def convert_images_to_png_task(file_paths):
    convert_to_png(file_paths, os.path.join(settings.MEDIA_ROOT, 'pngs'))

def convert_to_tiff(file_paths, output_path):
    imgs = []

    for file in file_paths:
        im = Image.open(file).convert('RGB')   
        imgs.append(im)

    
    if not imgs:
        raise ValueError(f"No valid images to save for {output_path}")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    imgs[0].save(
        output_path,
        save_all=True,
        append_images=imgs[1:]
    )

    File.objects.create(content_type="image/tiff", file_type="extracted", file_format="tiff", file_name=os.path.basename(output_path), file_location=output_path)

    return output_path

def convert_to_png(file_paths, output_paths):
    os.makedirs(output_paths, exist_ok=True)

    outputs = []
    for i, file in enumerate(file_paths):
        im = Image.open(file).convert('RGB')
        out = os.path.join(output_paths, f"output_{i}.png")
        im.save(out, "PNG")
        outputs.append(out)

        ext = os.path.splitext(out)[1].lstrip(".")
        File.objects.create(content_type="image/png", file_type="extracted", file_format="png", file_name=os.path.basename(out), file_location=out)

    return outputs