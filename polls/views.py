from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
from django.conf import settings
from .tasks import convert_images_to_pdf_task, convert_images_to_png_task, convert_images_to_tiff_task
from celery.result import AsyncResult
from cleantext import clean
import language_tool_python
import re

tool = language_tool_python.LanguageTool('en-US')

ALLOWED_TYPES = (
    'image/',
    'application/pdf',
)
# Create your views here.

def index(request):
    return render(request, "polls/index.html")

def upload_images(request):
    if request.method == "POST":
        files = request.FILES.getlist('file')
        action = request.POST.get("action")
        if not files:
            return JsonResponse({'success': False, 'error': 'No file was uploaded'})
        
        images_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        os.makedirs(images_dir, exist_ok=True)  

        file_paths = []

        for file in files:
            if not any (file.content_type.startswith(t) for t in ALLOWED_TYPES):
                return JsonResponse({'success': False, 'error': f'Uploaded file {file.name} was not in the correct format'})
            file_path = os.path.join(images_dir, file.name)
            with open(file_path, 'wb+') as destination: 
                for chunk in file.chunks():
                    destination.write(chunk)

            file_paths.append(file_path)

        if action == 'generate-pdf':    
            result = convert_images_to_pdf_task.delay(file_paths)
        elif action == 'generate-tiff':
            result = convert_images_to_tiff_task.delay(file_paths)
        elif action == 'generate-png':
            result = convert_images_to_png_task.delay(file_paths)
        else:
            return JsonResponse({'success': False, 'error': 'Unknown action'})
        
        print(result)
        request.session['task_id'] = result.id  
        request.session['action'] = action      
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_generated_file(request):
    task_id = request.session.get('task_id')
    action = request.session.get('action')

    if not task_id or not action:
        return redirect('index')
    
    task_result = AsyncResult(task_id)

    if action == 'generate-pdf':
        output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'output.pdf')
        file_url = settings.MEDIA_URL + 'pdfs/output.pdf'
    elif action == 'generate-tiff':
        output_path = os.path.join(settings.MEDIA_ROOT, 'tiffs', 'output.tiff')
        file_url = settings.MEDIA_URL + 'tiffs/output.tiff'
    elif action == 'generate-png':
        output_path = os.path.join(settings.MEDIA_ROOT, 'pngs', 'output.png')
        file_url = settings.MEDIA_URL + 'pngs/output.png' 

    if task_result.status == 'SUCCESS' and os.path.exists(output_path):
        return redirect(file_url)
    else:
        return render(request, 'polls/file_generation_in_progress.html') 
    

def file_generation_in_progress(request):
    return render(request, 'polls/file_generation_in_progress.html')

#clean text
def get_text_cleaner(request):
    return render(request, 'polls/text_cleaner.html')

def clean_text(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if not text: 
            return JsonResponse({'result': False, 'error': 'Invalid request method'})
        
        text = normalize_text(text)
        cleaned_text = clean(text,
            fix_unicode=True,       
            to_ascii=False,         
            lower=False,              
            no_line_breaks=False,   
            no_urls=False,         
            no_emails=False,        
            no_phone_numbers=False, 
            no_numbers=False,
            no_digits=False,
            no_currency_symbols=False,
            no_punct=False
        )
        #grammar correction
        matches = tool.check(cleaned_text)
        correct_text = language_tool_python.utils.correct(cleaned_text, matches)

        return JsonResponse({'result': True, 'correct_text': correct_text})
    return JsonResponse({
        'result': False,
        'error': 'Invalid request method'
    }, status=405)

def normalize_text(text):
    text = re.sub(r'([,.!?])([A-Za-z])', r'\1 \2', text)
    text = re.sub(r"\b(\w+)' (\w+)\b", r"\1'\2", text)
    text = re.sub(r"\s*'\s*", "'", text)
    text = re.sub(r"\bi\b", "I", text)
    return text.strip()
