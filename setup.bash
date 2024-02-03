#!/bin/bash
# ------------------------------------- Update and upgrade -------------------------------------#
sudo apt update
sudo apt upgrade

# install nginx
sudo apt install -y supervisor nginx

# install required packages 
#? maybe move these into the virtual environment
sudo apt install -y python3-picamera2 python3-readchar
sudo apt install -y python3-pyqt5 python3-opengl python3-venv
sudo apt install -y python3-opencv opencv-data



#------------------------------------- Copying configuration files -------------------------------------#
# set nginx settings by replacing default file
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
sudo cp ./nginx/fastapi-app.conf /etc/nginx/sites-available/fastapi-app

# copy webserver files to /var/www/cam
sudo mkdir -p /var/www/cam
sudo cp -a ./webserver/. /var/www/cam/

# copy supervisor configuration file
sudo cp supervisor.conf /etc/supervisor/conf.d/fastapi-app.conf

#------------------------------------- Setting up the webserver -------------------------------------#
# enable supervisor start at boot
sudo systemctl enable supervisor

# enable the fastapi-app configuration
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status fastapi-app



# restart the nginx service after settings set
sudo nginx -t
sudo service nginx restart

# create and setup virtual environment
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate



