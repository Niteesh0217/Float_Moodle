# Float-Moodle
Welcome to our CS 251 Course Project. This repository contains the code for a website which is a simple learning environment.

The following will help you to install and run this website on your local machine after cloning this repository.

```
$ cd Float-Moodle/
$ sudo apt install python3.8-venv
$ python3 -m venv project-env
$ source project-env/bin/activate
```
Then after activating the virtual environment, download the required dependencies.

``` $ pip install -r requirements.txt```

Then you are ready to run the server. 

```
$ cd float-moodle/
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```
