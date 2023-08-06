========================
Django Easy Subscription
========================

A Django application that provides a subscription pop-up form, and can be integrated with multiple email marketing platforms.

.. contents::
    :local:
    :backlinks: none


Installation
============

1. ``pip install django-easy-subscription``
2. Add ``easy_subscription`` to ``INSTALLED_APPS``
3. Run `python manage.py migrate` to create the subscriber model.
4. Add an URL entry to your project's ``urls.py``, for example::

    from django.conf import settings

    if 'easy_subcription' in settings.INSTALLED_APPS:
        urlpatterns += [
            path('easy-subscription/', include('easy_subscription.urls')),
        ]

Note: you can use whatever you wish as the URL prefix.


