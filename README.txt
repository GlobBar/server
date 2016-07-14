0. Install Linux, Apache, MySQL https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-ubuntu-14-04

1. After cloning project
   Create config from dist file - 
   <dev style="background-color: #292b36; color:#fff; border-radius: 3px;">
   cd ProjectName
   cp nightlife/settings.py.dist nightlife/settings.py
   </div>

2. in settings.py set database access parameters DATABASES ('USER' : 'userName', 'PASSWORD' : 'upassword' )	

3. Create a virtualenv to isolate our package dependencies locally
   <dev style="background-color: #292b36; color:#fff; border-radius: 3px;">
   sudo apt-get install virtualenv
   virtualenv 'nightlifeenv'
   source nightlifeenv/bin/activate</div>  # On Windows use `env\Scripts\activate`

4. <dev style="background-color: #292b36; color:#fff; border-radius: 3px;">sudo apt-get install libmysqlclient-dev</div>

5. Install dependencies  <dev style="background-color: #292b36; color:#fff; border-radius: 3px;">pip install -r requirements.txt</div>

6. Now sync your database for the first time: <dev style="background-color: #292b36; color:#fff; border-radius: 3px;">python manage.py migrate</div>

7. We'll also create an initial user named admin with a password of password123. We'll authenticate as that user later in our example.
   python manage.py createsuperuser

8. Start server - <dev style="background-color: #292b36; color:#fff; border-radius: 3px;">python manage.py runserver</dev>

9. got to http://mysyte.com    (login: admin, password: password123)