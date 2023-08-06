import os
from setuptools import setup, find_packages


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def get_doc():

    with open("README.md", "r") as fh:

        return fh.read()


setup(
    name="django_restframework_2fa",
    version="0.0.16",
    description="A simple two factor authentication plugin for DRF compatible to work with Twilio's SMS service..",
    long_description=get_doc(),
    long_description_content_type="text/markdown",
    url="https://github.com/jeetpatel9/django-restframework-2fa.git",
    author='Jeet Patel',
    author_email='jpatel99967@gmail.com',
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        "djangorestframework==3.12.4",
        "django==3.2.4",
        "twilio==6.55.0",
        "djangorestframework-simplejwt==4.6.0",
    ],
    extra_requires={
        "dev": [
            "mysqlclient==1.4.6",
            "pytest>=3.7",
            "twine 3.4.1",
        ]
    }
)
