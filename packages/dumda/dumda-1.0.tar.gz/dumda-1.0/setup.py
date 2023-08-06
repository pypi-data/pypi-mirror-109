from setuptools import setup
from setuptools import find_packages


setup(name='dumda',
      version='1.0',
      description='generate highly customizable dummy data for data science testing',
      keywords='data science python',
      url='https://github.com/oliverbdot/dumda',
      author='Oliver B.',
      author_email='oliverbcontact@gmail.com',
      license='MIT',
      packages=['dumda'],
      include_package_data=True,
      zip_safe=False)