## Description
In this document are listed configuration files with settings 
for nginx and Gunicorn.

## Technologies
* Nginx (1.10.3)
* Gunicorn (19.9.0)


## Basic Gunicorn installation and configuration
### Install Gunicorn
```
pip install gunicorn
```
### Creating systemd Socket and Service Files for Gunicorn

* Create and open a systemd service file for Gunicorn with sudo privileges
```
sudo nano /etc/systemd/system/gunicorn.service
```

```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=<your_admin_account>
Group=www-data
WorkingDirectory=/home/<your_admin_account>/moneta/moneta/src/python
ExecStart=/home/<your_admin_account>/.pyenv/versions/<moneta_venv>/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          moneta.wsgi:application

[Install]
WantedBy=multi-user.target
```

* Start and enable the Gunicorn socket. 
This will create the socket file at `/run/gunicorn.sock` now and at boot. 
When a connection is made to that socket, 
`systemd` will automatically start the `gunicorn.service` to handle it:
``` 
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

* Check the status of the process to find out whether it was able to start:
``` 
sudo systemctl status gunicorn.socket
```
* Check for the existence of the `gunicorn.sock` file within the `/run` directory:

```
file /run/gunicorn.sock
```
```
[Output]
/run/gunicorn.sock: socket
```

## Basic Nginx installation and configuration
### Install Nginx
```
sudo apt install nginx
sudo service nginx start   # start nginx
```

### Configure Nginx

* Add a new configuration file named `moneta_nginx.conf` 
inside `/etc/nginx/sites-available/`:
```commandline
sudo nano /etc/nginx/sites-available/moneta_nginx.conf
```

* Open a file called `moneta_nginx.conf`
in the `~/moneta/moneta/etc/` directory, copy its content and put this 
into `/etc/nginx/sites-available/moneta_nginx.conf`.
Replace `<your_admin_account>` with your value.

* Create log files
```commandline
mkdir /home/<your_admin_account>/logs/
cd /home/<your_admin_account>/logs/
touch nginx-access.log
touch nginx-error.log
```

* Test your Nginx configuration for syntax errors by typing:

```commandline
sudo nginx -t
```

* Save and close the file when you are finished. Now, we can enable the file by linking it to the sites-enabled directory:
```commandline
sudo ln -s /etc/nginx/sites-available/moneta_nginx.conf /etc/nginx/sites-enabled/moneta_nginx.conf
```

* Remove the default NGINX website:
```commandline
sudo rm /etc/nginx/sites-enabled/default
```


* Restart the NGINX service:
```commandline
sudo service nginx restart
```
