from setuptools import setup
import os

README = os.path.join(os.path.dirname(__file__), 'README.md')

setup(name='ninja-authentication',
      version='0.32',
      description='A package with builtin authentication apis and Base Emails',
      long_description='Link : https://github.com/EnzoCp/ninja-auth/tree/master/django_ninja_authentication',
      author='Enzo Pascucci',
      author_email='enzocpascucci@pascuccidevelopments.com',
      license='MIT',
      py_modules=['ninja-auth'],
      zip_safe=False,
      platforms='any',
      include_package_data=True,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Framework :: Django :: 3.2',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries'
      ],
      url='https://github.com/EnzoCp/ninja-auth'
      )