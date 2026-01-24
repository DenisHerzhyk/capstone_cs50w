# Multiapp: File Converter & Text Cleaner

## Distinctiveness and Complexity

This project satisfies the distinctiveness and complexity requirements by combining two backend-focused features into a single Django application.

The **File Converter** allows users to convert uploaded files into **PDF, TIFF, and PNG** formats. It uses **Celery** with **Redis** to process file conversions asynchronously, keeping the Django application responsive. The project involves file system management, directory creation, and handling multiple libraries for reading and generating files.

The **Text Cleaner** processes raw text through normalization steps such as punctuation cleanup, whitespace fixing, Unicode correction, and grammar checking using a Java-based language engine. This demonstrates non-trivial backend logic and integration between Python and external tools.

The project is complex due to:
- Asynchronous background tasks with Celery
- Redis integration
- File and directory management
- Use of multiple backend libraries
- Separation of concerns between conversion, text processing, and persistence

---

## Files Overview

### Root Directory
- `manage.py` – Django command-line utility
- `db.sqlite3` – Development database
- `media/` – Generated files (created during conversion)
- `static/` – CSS and images
- `node_modules/` – JavaScript dependencies
- `package.json` – JavaScript package configuration
- `postcss.config.js` – PostCSS configuration
- `tailwind.config.js` – Tailwind CSS configuration
- `README.md` – Project documentation

---

### `mysite/`
- `settings.py` – Django settings
- `urls.py` – Root URL configuration
- `asgi.py` / `wsgi.py` – Deployment entry points
- `celery_app.py` – Celery configuration and task discovery

---

### `polls/`
- `admin.py` – Django admin model registration
- `apps.py` – Application configuration
- `models.py` – Models for file metadata and cleaned text
- `tasks.py` – Celery tasks for file conversion
- `views.py` – Request handling logic
- `urls.py` – Application URL routes
- `templates/` – HTML templates
- `migrations/` – Database migrations

---

### Templates (`polls/templates/polls/`)
- `layout.html` – Base layout template
- `index.html` – Main page of the application
- `text_cleaner.html` – Text cleaning interface
- `file_generation_in_progress.html` – Status page shown during file conversion

---

### URLs (`polls/urls.py`)
- `/` – Main index page
- `/upload/` – Upload files for conversion
- `/file_generation_in_progress/` – Conversion progress page
- `/get_generated_file/` – Retrieve generated files
- `/text_cleaner/` – Text cleaner page
- `/clean/` – Text cleaning request endpoint

---

## How to Run the Application

### Package JSON
```bash
npm install
```

### Redis
```bash
redis-server --port 6380 --bind 127.0.0.1
```

### Celery
```bash
celery -A mysite.celery_app worker --loglevel=info
```

### Django
```bash
python manage.py runserver
```

##Tailwind
```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```