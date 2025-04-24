apt-get install apache2 libapache2-mod-wsgi-py3 mysql-server libmysqlclient-dev python3-dev build-essential python3-venv pkg-config
git clone https://github.com/amschaal/slims-django.git /var/www/slims
cd /var/www/slims
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Database Setup (localhost)
```
CREATE DATABASE slims;
CREATE USER 'slims'@'localhost' IDENTIFIED BY 'SOMEPASSWORD';
GRANT ALL privileges ON slims.* TO 'slims'@'localhost';
FLUSH PRIVILEGES;
```

# Import existing database from old app
mysql slims < ../slims_backup.sql

# Copy config.example.py to config.py and edit

# Run migrations w/ --fake-initial
python manage.py migrate --fake-initial

# Collect static files
python manage.py collectstatic

# Setup apache: copy and edit apache.example.conf to site-available, then symlink from sites-enabled
c