# update and upgrade the system
sudo apt update
sudo apt upgrade

# install nginx
sudo apt install -y nginx

# install required packages
sudo apt install -y python3-picamera2
sudo apt install -y python3-pyqt5 python3-opengl
sudo apt install -y python3-opencv opencv-data

# set nginx settings by replacing default file
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
sudo cp ./nginx/default.conf /etc/nginx/sites-available/default

# copy webserver files to /var/www/cam
sudo mkdir -p /var/www/cam
sudo cp -a ./webserver/. /var/www/cam/

# restart the nginx service after settings set
sudo service nginx restart
sudo /etc/init.d/nginx start
