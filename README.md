# WANNA SEE IT?

## Installation

Prerequisites:

* [Python](https://www.python.org/) (2.7 recommended)
* [pip](https://pypi.python.org/pypi/pip)
* Database of your choice ([Postgresql](http://www.postgresql.org/) recommended)

Quick start:

* Install dependencies
* Clone the repository
* Copy `settings.py.default` to `settings.py` and modify as appropriate - in particular you'll need to create and configure a database
* Run `python manage.py migrate`
* Run `python manage.py runserver`
* Open <http://localhost:8000/>

## Notes

* The API is implemented with [Django REST framework](http://www.django-rest-framework.org/) - this toolkit allows very fine-grained control over the API. As a nice side-effect, it includes a fully functional web browseable view of the API.
* Only supported authentication currently is Django auth - requiring a valid Django session and sending of CSFR tokens. Obviously this is not ideal, but can be expanded relatively easily through additional [authentication schemes](http://www.django-rest-framework.org/api-guide/authentication/) - and works just fine for the web browseable API.

## Design decisions

Some of these decisions may be difficult to grok just from reading the code, so I've detailed them below:

* Overall API entry point is /api/v1 - my understanding is that this nomenclature is fairly standard, and allows future versions of the API to be shipped independently. A root view allows some API discovery.
* Throughout the API, hyperlinks provide a path to related objects.
* User registration is explicitly restricted to non-logged-in users.
* Only admin users can view a list of all users - this functionality is not really required for an app.
* Users can look at a "details view" of another user - but this contains a very small set of information (currently only username).
* If users view their own details, a larger set of information is exposed.
* Anyone (even anonymous users) can view a list of posts, or details about an individual post.
* The post list performs pagination, based on a cursor - this is a built-in feature of DRF, but means that a user won't see the same post multiple times on subsequent pages if new posts have appeared in the meantime. This will be particularly important for this application, where posts will be occuring frequently.
* Posts include a link to retrieve the image for that post.
* Images are served from offline storage, in a very controlled fashion: Anonymous users cannot view images. Logged-in users can view images once, then a flag is recorded that prevents them from seeing that image again.

## Reading the code

* Models are defined in `home/models.py`
* API URL schemes are defined in `home/api/urls.py`
* These map to views, defined in `home/api/views.py`
* Views take advantage of serializers (`home/api/serializers.py`) to move data back and forth between clients and models
* Take particular note of permission_classes in view definitions - these define who can access a given view or action (custom permissions in `home/api/permissions.py`)
