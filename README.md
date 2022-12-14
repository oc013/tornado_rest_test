Intro
-----
This is an evaluation of the Tornado framework/web server.

We'll create a simple application for creating and counting any number of widgets.

A REST API will be created/exposed to allow CRUD operations on the singular table in the system.

A basic HTML/JS client will be presented so we don't need something like Postman to interface with the API.

Requirements
------
Python 3.8.13

Install
------
```
git clone https://github.com/oc013/tornado_rest_test.git
cd tornado_rest_test
pip install -r requirements.txt
python main.py
```

Browse to http://localhost:8000/

Attributions
------
Favicon by [Lorc](https://game-icons.net/1x1/lorc/tornado.html) under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)

Todo
------
* Write unit tests
* Add async/await on server side?
* Dockerfile?

* ~~Devise a logical way to organize backend code e.g. controller vs model type classes~~
* ~~Determine if we want to have multiple routes under /api within the same class~~
* ~~Create form and related js to make it a self-contained system~~
* ~~Add/expose all the endpoints for the api~~
* ~~Server side data validation - display something on client side~~
* ~~Validate name field is limited to 64 characters~~
* ~~protect from SQL injection etc~~
* ~~PEP8 compliance - keeping it in mind~~
