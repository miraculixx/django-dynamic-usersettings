import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django_dynamic_usersettings',
    version='0.1',
    packages=['django_dynamic_usersettings'],
    include_package_data=True,
    install_requires=['django-tastypie'],
    license='MIT',
    url='https://github.com/miraculixx/django-usersettings/',
    description='Generic settings and API for Django.',
    long_description=README,
    author='miraculixx, Dryice Liu',
    author_email='miraculixx@gmx.ch, dryiceliu@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
