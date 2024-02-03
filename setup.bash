# update and upgrade the system
sudo apt update
sudo apt upgrade

# install nginx
sudo apt install -y supervisor nginx

# install required packages
sudo apt install -y python3-picamera2 python3-readchar
sudo apt install -y python3-pyqt5 python3-opengl python3-venv
sudo apt install -y python3-opencv opencv-data




# set nginx settings by replacing default file
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
sudo cp ./nginx/default.conf /etc/nginx/sites-available/default

# copy webserver files to /var/www/cam
sudo mkdir -p /var/www/cam
sudo cp -a ./webserver/. /var/www/cam/

# start supervisor
sudo systemctl enable supervisor




# restart the nginx service after settings set
sudo service nginx restart
sudo /etc/init.d/nginx start


