After cloning project
1. cd ProjectName
2. Create a virtualenv to isolate our package dependencies locally
   virtualenv 'nightlifeenv'
   source nightlifeenv/bin/activate  # On Windows use `env\Scripts\activate`
3. Install dependencies  pip install -r requirements.txt
4. Now sync your database for the first time: python manage.py migrate
5. We'll also create an initial user named admin with a password of password123. We'll authenticate as that user later in our example.
   python manage.py createsuperuser
6. got to http://mysyte.com    (login: admin, password: password123)

