import os;

os.remove("db.sqlite3")
os.system("python manage.py makemigrations")
os.system("python manage.py migrate")
# os.system("python manage.py createsuperuser")
os.system('''python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'poopy!')"''')
# os.system("admint")
# os.system("poopy!")
os.system("python manage.py runserver")