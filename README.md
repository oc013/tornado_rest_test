Intro
-----
This is a simple application to evaluate the Tornado framework/web server.

We'll create a simple application for creating and counting any number of widgets.

A REST API will be created/exposed to allow CRUD operations on the singular table in the system.

A very basic HTML/JS form will be presented on the front end so we don't need something like Postman to interface with the API.

Requirements
------
Python 3.8.13

Install
------
git clone --- https://github.com/oc013/tornado_rest_test.git
pip install -r requirements.txt
python main.py

Attributions
------

Favicon by Lorc https://game-icons.net/1x1/lorc/tornado.html under CC BY 3.0 https://creativecommons.org/licenses/by/3.0/


Todo
------
* Devise a logical way to organize backend code e.g. controller vs model type classes
* Create form and related js to make it a self-contained system
* Add/expose all the endpoints for the api
* * Determine if we want to have multiple routes under /api within the same class
* Write tests
* Verify we
* Dockerfile?