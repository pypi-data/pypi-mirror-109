===========================
Django Ninja Authentication
===========================

Authentication Views and authentication method to you django-ninja project


Quick Start
===========
1. Add 'django_ninja_auth' to your INSTALLED_APPS setting like the following:

.. code-block:: python

    INSTALLED_APPS = [
    ... 'ninja_authentication',
    ]


1. Add NINJA_AUTH_CONFIG on your setting like the following:
=====
.. code-block:: python

    NINJA_AUTH_CONFIG = {
    'ACCESS_TOKEN_EXPIRE_MINUTES': 60 * 24 * 31,
    'ACCESS_TOKEN_EXPIRE_HOURS': 24 * 31,
    'ACCESS_TOKEN_EXPIRE_DAYS': 31,
    'SIGNUP_SCHEMA': SignupSchema,
    'USERNAME_FIELD': 'username',
    'SEND_WELCOME_MAIL': True,
    'WELCOME_MAIL_SUBJECT': 'Bem vindo!',
    'WELCOME_MAIL_TEMPLATE': 'welcome.html',
    'DOMAIN': 'localhost',
    'PROTOCOL': 'http',
    }

- Token Expire (CHOOSE ONLY ONE OF THEM)(OPTIONAL)
    - ACCESS_TOKEN_EXPIRE_MINUTES requires amount in minutes
    - ACCESS_TOKEN_EXPIRE_HOURS requires amount in hours
    - ACCESS_TOKEN_EXPIRE_DAYS requires amount in days
    - If not set the package will get the default, which is 1 day

- SIGNUP_SCHEMA(MANDATORY)
    - Its the schema for the Signup view/api

- SEND_WELCOME_MAIL (OPTIONAL)
    - if True it requires
    - WELCOME_MAIL_SUBJECT
    - WELCOME_MAIL_SUBJECT

- Domain (MANDATORY)
    - Used for the reset password api

- Protocol (MANDATORY)
    - User for the reset password api

- RESET_PASSWORD_TEMPLATE (MANDATORY)
    - Template for the Reset Password email
    - Template must have the following line:

.. code-block:: python

    <a href="{{ protocol|safe }}://{{ domain|safe }}:8000/apis/auth/reset/{{ uid|safe }}/{{ token|safe }}">Mudar minha senha</a>


- Do not forget to set email config on django

2. Add router to you api
========================

3. run python manage.py migrate to create authtoken model
==========================================================

Add-Ons
========

- BaseHtmlMessageEmail is a base hmtml email using threading to boost your project!
How to Use:
===========
- email, template_name, subject (REQUIRED)
- context must be a dictionary and is optional