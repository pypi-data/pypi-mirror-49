from setuptools import setup, find_packages
import sys, os

version = '4.5'

setup(name='cssocialprofile',
      version=version,
      description="SocialProfile app extension",
      long_description=open("README.rst").read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Josu Azpillaga',
      author_email='jazpillaga@codesyntax.com',
      url='http://www.codesyntax.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'social-auth-app-django',
          'django-registration-redux',
          'tweepy',
          'pyfacebook',
          'django-photologue',
          'Django>=1.10'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
