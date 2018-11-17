import codecs
import os
import re

from setuptools import setup


setup(
    name='django-indexes',
    version=version,
    description=(
        'This package suggests db indexes by analysing sql queries.'
    ),
    url='https://github.com/ottoyiu/django-cors-headers',
    packages=['django_indexes'],
    license='MIT License',
    keywords='django indexes',
    platforms=['any'],
    install_requires=[
        "redis==3.0.1",
        "sqlparse==0.2.4"
    ],
    python_requires='>=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    classifiers=[
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
