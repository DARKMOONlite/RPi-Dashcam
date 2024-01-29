
sudo apt update
sudo apt upgrade


sudo apt install nginx
sudo /etc/init.d/nginx start


# set nginx settings by replacing default file
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
sudo cp ./nginx/default /etc/nginx/sites-available/default
# sudo sed  -i 's/root \/var\/www\/html;/~\/Git\/RPi-Dashcam\/webserver;/g' /etc/nginx/sites-available/default
# restart the nginx service after settings set
sudo service nginx restart
