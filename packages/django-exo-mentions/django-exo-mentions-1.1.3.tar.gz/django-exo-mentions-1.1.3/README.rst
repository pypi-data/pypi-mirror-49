=============================
django-exo-mentions
=============================

.. image:: https://badge.fury.io/py/django-exo-mentions.svg
    :target: https://badge.fury.io/py/django-exo-mentions

.. image:: https://requires.io/github/exolever/django-exo-mentions/requirements.svg?branch=master
     :target: https://requires.io/github/exolever/django-exo-mentions/requirements/?branch=master
     :alt: Requirements Status

.. image:: https://travis-ci.org/exolever/django-exo-mentions.svg?branch=master
    :target: https://travis-ci.org/exolever/django-exo-mentions

.. image:: https://codecov.io/gh/exolever/django-exo-mentions/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/exolever/django-exo-mentions

.. image:: https://sonarcloud.io/api/project_badges/measure?project=exolever_django-exo-mentions&metric=alert_status
   :target: https://sonarcloud.io/dashboard?id=exolever_django-exo-mentions


Documentation
-------------

The purpose of this package is to handle in some way mentions to users in a text field of a model. You can choose the model you want, the field you want to listen to mentions, the pattern you use to codify the mention and the callback to notify to your app.

The package will notify to callback function each time there is a mention in this field of the model. Then you can act accordingly on your application requisites.

The full documentation is at https://exo-mentions.readthedocs.io.

Quickstart
----------

Install django-exo-mentions::

    pip install django-exo-mentions

=====
Usage
=====

To use django-exo-mentions in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'exo_mentions',
        ...
    )

Define a signal for the callback

.. code-block:: python

    from django.dispatch import receiver
    from django.core.signals import request_finished

    @receiver(request_finished)
    def post_detect_mention_callback(sender, **kwargs):
        """ You will receive information of the mention
        user_from: kwargs.get('user_from')
            User that mentions
        object_pk: kwargs.get('object_pk')
            User's Pk that has been mentioned
        target: kwargs.get('target')
            The object where the mention was made
        """

        # Your code here

Register a model and field in which you want to detect mentions.
You can override the pattern if you want.

.. code-block:: python

    from django.apps import AppConfig
    from exo_mentions.registry import register

    class MyAppConfig(AppConfig):
        name = 'myapp'

        def ready(self):
            model = Post
            field = 'description'
            callback = post_detect_mention_callback

            register(model, field, callback)

At this point the library will notify to the callback each time there is a mention in the field of the registered model. Thats all! :)

.. code-block:: python

    def register(model, field, callback, pattern):
    """
    This method handles the mentions about the model in the field and notify to the callback when there is any mention

    Parameters
    ----------
    model : Models
        The model to register for detect mentions
    field : str
        Field of the model to detect mentions
    callback : function
        Callback function to notify when there are mentions
    pattern : regular expression
        The pattern to codify the mentions (default r'class="mention" data-user=[\'"]?([^\'" >]+)')
    """


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
