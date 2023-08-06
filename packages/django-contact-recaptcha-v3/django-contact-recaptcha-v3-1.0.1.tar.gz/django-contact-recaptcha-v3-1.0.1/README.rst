====================
Django Contact Form
====================

Django-contact-form is a simple Django Contact Form with Google Recaptcha v3 - integration.

Quick start
-----------

1. Add "form" to your INSTALLED_APPS setting like this::

	 INSTALLED_APPS = [
        	...
        	'contact-form',
	]

2. Include the polls URLconf in your project urls.py like this::

	path('', include('contact-form.urls')),

3. Run `python manage.py migrate` to create the form models.

4. For finding Templates add this line into TEMPLATES in settings.py::

	TEMPLATES = [
             {
              ...
             'DIRS': [os.path.join(BASE_DIR, 'templates')],
              ...
             }
         ]

5. To setup Email and Recaptcha just paste this code with your keys in settings.py::

         EMAIL_HOST = 'smtp.foo.com'
         EMAIL_USE_TLS = True
         EMAIL_PORT = 587
         EMAIL_HOST_USER = 'foo@gfoo.com'
         EMAIL_HOST_PASSWORD = 'swordfish'

         RECAPTCHA_SITE_KEY = ""
         RECAPTCHA_SECRET_KEY = ""

6. Visit http://127.0.0.1:8000/contact/ to check the contact-form.
