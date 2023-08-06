import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

REQUIREMENTS = [
    'Django>=2.0.0',
    'django-countries-with-calling-codes>=0.1',
    'py3dns>=3.2.0',
]


setup(
    name='django-easy-subscription',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description=(
        'A Django application that provides a subscription pop-up form, '
        'and can be integrated with multiple email marketing platforms.'
    ),
    long_description=README,
    url='https://github.com/rondebu/django-easy-subscription',
    author='Rondebu Software',
    author_email='info@rondebu.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
