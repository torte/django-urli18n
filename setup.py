from setuptools import setup, find_packages

setup(
      name='django-urli18n',
      version='0.1',
      description='A reusable Django app to display the current activated language in the URL',
      author='Torsten Engelbrecht',
      author_email='torsten.engelbrecht@gmail.com',
      url='https://github.com/Torte/django-urli18n',
      download_url='https://github.com/Torte/django-urli18n/tarball/master',
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
        'Environment :: Web Environment',
        "Programming Language :: Python",
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)