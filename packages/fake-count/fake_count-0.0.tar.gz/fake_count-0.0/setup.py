import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='fake_count',
      version='0.0',
      description='Django app for displaying a random number based on the time of day.',
      packages=['fake_count'],
      include_package_data=True,
      license='BSD License',
      long_description=README,
      url='https://github.com/pro100git/django_fake_counter',
      author_email='bsana7931@gmail.com',
      zip_safe=False)