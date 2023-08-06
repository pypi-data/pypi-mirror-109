<h1> DRF Two Factor Authentication. </h1>

A simple two factor authentication plugin for <a href="https://www.django-rest-framework.org/">Django Rest Framework</a> built on top of <a href="https://pypi.org/project/djangorestframework-simplejwt/">Simple JWT</a> and compatible with Twilio's SMS service. 

The motive of ***DRF Two Factor Authentication*** is to provide the pre defined basic authentication related APIs. It aims to cover the most common use case of ***Two Factor Authentication*** by providing the set of most generic APIs. This plugin will only work with Twilio's SMS service.

## Acknowledgments

It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).


## Content

- Requirements
- Installation
- Usage



## Requirements 

- Python (3.7, 3.8, 3.9)
- Django (3.2.4)
- Django Rest Framework (3.12.4)
- Django Rest Framework Simple JWT (4.6.0)
- Twilio (6.55.0)

## Installation

DRF Two Factor Authentication can be installed with pip:

```
pip install django-restframework-2fa
```


Then, your django project must be configured to use the plugin <a href="https://pypi.org/project/djangorestframework-simplejwt/">Simple JWT<a>. It is highly recommended to appropriately configure this plugin as this package is highly dependent on it.