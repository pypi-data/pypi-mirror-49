=====
Users
=====

Users is a simple Django app that create own custom users and a RESTful API for the users that is allauth enabled.

Quick start
-----------

1. Add "users" to your INSTALLED_APPS setting like this::

	INSTALLED_APPS = [
		...
		'customusers',

	]

2. Include the usres URLconf in your project urls.py like this::

    path('users/', include('customusers.urls')),

3. Run `python manage.py migrate` to create the users models.

4. Start the development server and visit http://127.0.0.1:8000/users/
   to view the users API

