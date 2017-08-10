# PAWS Image service

PAWS Image service is a third-party web-service application with RESTAPI and 
simple web-UI interface that works like an internal web repository for Windows 
QCOW images pre-configured and ready to be consumed by PAWS. 

It is an optional component for PAWS and does not require PAWS installed at 
the same system it is running. 

The purpose of PAWS Image service is to allow you to manage your internal 
and self-maintained repository of QCOW Windows images pre-configured with your
environment and allow your PAWS users to run Windows systems in their local 
standalone virtual machines that we strong recommend using Libvirt QEMU-KVM 
as provider.

Examples of usage for PAWS image service and running Windows locally as 
virtual machines: 

* pre-validation of your Windows QCOW images before to make than available in 
a cloud environmnet.
* share Windows pre-defined images with an internal team for quick tests and 
with ability to run in off-line ( all in a local virtual machine )
* developing new Powershell scripts to be consumed by PAWS during automation 
* Windows troubleshooting and debug
* when you don't have a cloud computing environment available and want to share
your own QCOW Windows images internally with your team

important
----------

* PAWS Image service doesn't provide any Windows QCOW Image with it.
* It is expected you know how to build your own Windows QCOW image.
* PAWS Image service doesn't have supply any MSDN license or any rights.

# Table of Contents
1. [Installation](#Installation)
2. [Usage](#Usage)


## Installation

OS supported: Fedora, CentOS and RHEL ( might need some package in others Linux 
distros )
Being tested: Fedora versions 24 to 26

clone this repo and install required python libraries. You might need to install
some extra packages in your system, check [devel packages](#Devel packages)

## Usage

### As user

You access URL of PAWS image service, or http://0.0.0.0:5000 if on development
mode, browse the images vailable in your internal repository, download them 
to your local machine to run the Windows in a local virtual environment.

### As system administrator

Copy /paws-imgsrv/imgsrv/imgsrv.properties.sample to 
/paws-imgsrv/imgsrv/imgsrv.properties and update the variables with your
needs. 

Follow the installation steps described above. Load /qcow folder with your
QCOW and xml files. 

You can run this as single standalone wsgi python process or behind a Nginx, 
Apache or any other compatible web-service.

For simple standalone python process:

```
cd paws-imgsrv/imgsrv
python app.py
```

or through wsgi single process:

```
cd paws-imgsrv/imgsrv
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi
```

to run behind a Nginx see /scripts/nginx and to run as systemctl daemon see
/scripts/systemctl

## Contributing

To setup your machine to work on paws-imgsrv is simple and easy. paws-imgsrv
is a standard Python web-service running on Flask framework and importing
basic python libraries. You might need to install some packages and pip libs 
as described below in next items. 

### Devel packages

You might need to have these packages in your system, othwerise proceed with 
the command below to install them:

```
sudo dnf install -y git git-review wget gcc make rpm-build python-devel \
python-setuptools python-pip python2-flake8 pylint python2-devel \
python-kitchen openssl-devel libffi-devel gcc python-oslo-serialization \
python-pep8 ansible krb5-workstation
```

### Python virtual environment

we recommend you running this application in a separated python virtual 
environment to avoid any library conflict. Create a python virtual environment, 
activate it and install required libs:

```
virtualenv -p /usr/bin/python2.7 venv_pawsimgsrv
source venv_pawsimgsrv/bin/activate
pip install -r requirements-dev-venv.txt --upgrade
```

### run the application

```
cd paws-imgsrv/imgsrv
python app.py
```

or through wsgi single process:

```
cd paws-imgsrv/imgsrv
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi
```

or in your Eclipse in project -> pydev -> create a new virtual environment
pointing to that you just created and set this to be the python libs for your
paws-imgsrv project.
 
 When application is running you can access by http://127.0.0.1:5000

### code check and analyze

Before any commit make sure your code changes are following the code standard
of this project running the command:

```
cd paws-imgsrv
make codecheck
```

### report an issues

To report an issue that can be ideas or suggestions for new features, or even
a bug, please follow github https://help.github.com/articles/creating-an-issue/

## Screenshots

Home-page

![Preview](https://github.com/rhpit/paws-imgsrv/raw/master/imgsrv/static/images/screenshot_3.png)

Listing images from internal repository
![Preview](https://github.com/rhpit/paws-imgsrv/raw/master/imgsrv/static/images/screenshot_1.png)

![Preview](https://github.com/rhpit/paws-imgsrv/raw/master/imgsrv/static/images/screenshot_1.png)


## License

It is under GNU GENERAL PUBLIC LICENSE version 3.0 as you have received a local
copy at LICENSE file
