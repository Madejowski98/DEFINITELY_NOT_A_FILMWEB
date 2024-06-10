pip install -r requirements.txt
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully."