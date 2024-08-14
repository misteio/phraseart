# Phraseart

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
django-admin startproject website

python -m pip install <package>

run : 
cd website
python manage.py runserver


pip install -r requirements.txt


python manage.py migrate


Opensearch:
Create index
python manage.py opensearch index create

Index Docs:
python manage.py opensearch document index
