from distutils.core import setup
import setuptools

requires = []

with open('requirements.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        requires.append(line)	
            

setup(name='postal_tracker',
      url='https://github.com/eitans96/Mail_Tracker',
      version='0.1.0',
      description='Mail Tracker service',
      author='Eitan Shaulson',
      author_email='eitanshaulson@gmail.com',
      install_requires=requires,
      scripts=['bin/mtracker'],
      packages=['postal_tracker'],
)
