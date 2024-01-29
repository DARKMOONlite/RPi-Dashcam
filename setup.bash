
sudo apt update
sudo apt upgrade


sudo apt install nginx
sudo /etc/init.d/nginx start

sed  -i 's/root \/var\/www\/html;/~\/Git\/RPi-Dashcam\/webserver;/g' /etc/nginx/sites-available/default