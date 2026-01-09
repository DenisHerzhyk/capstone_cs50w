from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
from django.conf import settings
from .tasks import convert_images_to_pdf_task
from celery.result import AsyncResult
from cleantext import clean

# Create your views here.

def index(request):
    return render(request, "polls/index.html")

def upload_images(request):
    if request.method == "POST":
        files = request.FILES.getlist('file')
        if not files:
            return JsonResponse({'success': False, 'error': 'No file was uploaded'})
        
        images_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        os.makedirs(images_dir, exist_ok=True)  

        file_paths = []

        for file in files:
            file_path = os.path.join(images_dir, file.name)
            with open(file_path, 'wb+') as destination: 
                for chunk in file.chunks():
                    destination.write(chunk)

            file_paths.append(file_path)

        result = convert_images_to_pdf_task.delay(file_paths)
        request.session['task_id'] = result.id
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def file_generation_in_progress(request):
    return render(request, 'polls/file_generation_in_progress.html')

def get_generated_file(request):
    task_id = request.session.get('task_id')
    if not task_id:
        return redirect('index')
    
    task_result = AsyncResult(task_id)
    pdf_output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', 'output.pdf')
    pdf_url = settings.MEDIA_URL + 'pdfs/output.pdf'

    if task_result.status == 'SUCCESS' and os.path.exists(pdf_output_path):
        return redirect(pdf_url)
    else:
        return render(request, 'polls/file_generation_in_progress.html') 
    
def get_text_cleaner(request):
    return render(request, 'polls/text_cleaner.html')

def clean_text(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if not text: 
            return JsonResponse({'result': False, 'error': 'Invalid request method'})
        
        cleaned_text = clean(text,
            fix_unicode=True,       
            to_ascii=True,         
            lower=True,              
            no_line_breaks=False,   
            no_urls=True,         
            no_emails=False,        
            no_phone_numbers=False, 
            no_numbers=False,
            no_digits=False,
            no_currency_symbols=False,
            no_punct=False
        )
        return JsonResponse({'result': True, 'cleaned_text': cleaned_text})
    return JsonResponse({
        'result': False,
        'error': 'Invalid request method'
    }, status=405)