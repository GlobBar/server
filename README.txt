0. Install Linux, Apache, MySQL https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-ubuntu-14-04

1. After cloning project
   Create config from dist file - 
   cd ProjectName 
   cp nightlife/settings.py.dist nightlife/settings.py

2. in settings.py set database access parameters DATABASES ('USER' : 'userName', 'PASSWORD' : 'upassword' )	

3. Create a virtualenv to isolate our package dependencies locally
   sudo apt-get install virtualenv
   virtualenv 'nightlifeenv'
   source nightlifeenv/bin/activate  # On Windows use `env\Scripts\activate`

4. sudo apt-get install libmysqlclient-dev

5. Install dependencies  pip install -r requirements.txt

6. Now sync your database for the first time: python manage.py migrate
7. We'll also create an initial user named admin with a password of password123. We'll authenticate as that user later in our example.
   python manage.py createsuperuser
8. got to http://mysyte.com    (login: admin, password: password123)