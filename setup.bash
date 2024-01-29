# update and upgrade the system
sudo apt update
sudo apt upgrade

# install nginx
sudo apt install nginx



# set nginx settings by replacing default file
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
sudo cp ./nginx/default /etc/nginx/sites-available/default

# copy webserver files to /var/www/cam
sudo mkdir /var/www/cam
sudo cp -a ./webserver/. /var/www/cam/

# restart the nginx service after settings set
sudo service nginx restart
sudo /etc/init.d/nginx start
