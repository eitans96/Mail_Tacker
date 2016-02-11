
from distutils.core import setup

setup(name='Mail_tracker',
      version='1.0',
      description='Mail Tracker service',
      author='Eitan Shaulson',
      author_email='eitanshaulson@gmail.com',
      py_modules = ['Mail_Tracker'],
      install_requires = ['BeautifulSoup4', 'datetime']
)
