from setuptools import setup
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Flask-Web-Log',
    version='0.1',
    url='https://github.com/nethunterslabs/flask-web-log',
    download_url="https://github.com/nethunterslabs/flask-web-log/archive/0.1.tar.gz",
    license='Apache 2.0',
    author='Nethunters Dev',
    author_email='dev@nethunters.co.uk',
    description='Enables web traffic and request logs for your Flask app.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['flask_web_log'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=1.0',
        'jsonpickle>=1.2',
        'SQLAlchemy>=1.3'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Flask',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
