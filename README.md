#Multiapp 

##Redis setup
Use following command to run **redis server**

`redis-server --port 6380 --bind 127.0.0.1`

##Celery setup
Use following command to run **celery server**

`celery -A mysite.celery_app worker --loglevel=info`

##Django
Use following command to run **django**

`python manage.py runserver`

##Tailwind
For styling you need to run **tailwindcss**

`npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch`