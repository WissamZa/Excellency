python manage.py makemigrations
python manage.py migrate
echo "from account.models import User; User.objects.create_superuser('admin', 'admin@Excellency.com', 'admin123')" | python manage.py shell
python manage.py runserver