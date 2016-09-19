from ubuntu:14.04

maintainer AdamJFurbee

#run echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
run apt-get update
run apt-get install -y build-essential git
run apt-get install -y python3 python3-dev python3-setuptools python3-pip
## run apt-get install -y supervisor
## #run easy_install pip
## 
## # install uwsgi now because it takes a little while
## run pip3 install uwsgi
## 
## # install nginx
## run apt-get install -y python-software-properties
## run apt-get install -y software-properties-common
## run apt-get update
## run add-apt-repository -y ppa:nginx/stable
## run apt-get update
## run apt-get install -y nginx
## run apt-get install -y sqlite3
## 
## # install our code
add . /home/docker/code/
## 
## # setup all the configfiles
## run echo "daemon off;" >> /etc/nginx/nginx.conf
## run rm /etc/nginx/sites-enabled/default
## run ln -s /home/docker/code/nginx.conf /etc/nginx/sites-enabled/
## run ln -s /home/docker/code/supervisor-app.conf /etc/supervisor/conf.d/
## 
## # run pip install
run pip3 install -r /home/docker/code/requirements.txt
## 
## # install django, normally you would remove this step because your project would already
## # be installed in the code/app/ directory
## run python3 /home/docker/code/manage.py makemigrations --noinput
## run python3 /home/docker/code/manage.py migrate --noinput
## run python3 /home/docker/code/manage.py collectstatic --noinput
## # run django-admin.py startproject website /home/docker/code/app/
## 
## expose 80
## cmd ["supervisord", "-n"]
