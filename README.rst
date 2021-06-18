=================
WaterBoard
=================

Getting Started
----------------

Clone the repo

.. code-block:: sh

    git clone https://github.com/okoisorjr/waterboard.git


Installation
-------------------------

You'll need to have virtual enviroment installed on your machine

.. code-block:: sh

    pip3 install virtualenv


Setup virtual environment

.. code-block:: sh

    virtualenv -p python3.8 .virtualenv

Activate virtual environment

.. code-block:: sh

    source .virtualenv/bin/activate


Install  Python3.8 development files

.. code-block:: sh

    sudo apt-get install python3.8-dev


Install the requirements. Ensure you have a linter config working on your code editor

.. code-block:: sh

    pip install -r requirements.txt


- Install `rabbitmq`

Run the following command

.. code-block:: sh

    sudo apt-get update & sudo apt install rabbitmq-server


Run migrations before starting the django-server

.. code-block:: sh

    python manage.py migrate

Starting Celery server

.. code-block:: sh

    celery -A wash worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

