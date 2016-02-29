Summary
-------
This is an API Proxy for the browser support and usage data from [CanIUse.com](http://caniuse.com/) hosted [here](https://github.com/fyrd/caniuse).

Built with [Flask](http://flask.pocoo.org/), it includes REST endpoints for the following: 
* A mapping to every browser feature listed [here](https://github.com/Fyrd/caniuse/tree/master/features-json).
* A search endpoint for the aforementioned features.
* [A HipChat Integration Hook](https://blog.hipchat.com/2015/02/11/build-your-own-integration-with-hipchat/). 

Implementation Notes
--------------------
The application follows the guidelines from [Flask Patterns for Large Applications](http://flask.pocoo.org/docs/patterns/packages/) using [Jinja](http://jinja.pocoo.org/) for view templating and Blueprints and Decorators for routing and dispatching. 

The front-end is styled using [Furtive](http://furtive.co). 

Setting up VirtualEnvWrapper
---------------------
It is **STRONGLY** recommended that you install and use [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html).

This is the basic how-to for Mac OSX:
```
$ sudo pip install virtualenvwrapper
$ mkdir ~/.py-virtual-env
$ export WORKON_HOME=~/.py-virtual-env
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv caniuse-api
$ workon caniuse-api
```

Running the App
---------------
After cloning your repo and setting up your virtual environment, install the Python dependencies by running [pip](https://pip.pypa.io/en/stable/installing/):
```
$ pip install -r requirements.txt
```
And install the front-end dependencies by running [bower](http://bower.io/):
```
$ bower install
```
There is limited (but growing!) test coverage. To run the tests:
```
$ nosetests
```
After installing dependencies and verifying that the tests are passing, start the app:
```
$ python runserver.py
```
And you should see the app running on your [localhost at port 5000](http://localhost:5000).

If you wish to expose the HipChat endpoint while running the project locally, you'll want to use [ngrok](http://ngrok.com/) to tunnel your localhost to a publicly accessible endpoint for your Integration hook. 

Local Config
------------
To set local configuration settings create the following file in your project directory:
```` 
$ touch settings.cfg
````
And then export it to your bash profile:   
```
$ export CANIUSE_API_CFG=$PWD/settings.cfg
```
In this project repository settings.cfg is un-versioned so it's an *excellent* place to put the Google OAuth Key and Secret as well as an auth token for the HipChat endpoint.

Go to the [Google Developer Console](https://code.google.com/apis/console) and create an API Key and Secret paired with your local [ngrok](http://ngrok.com/) url for callback. You may also want to create a pair of [GUIDs](https://www.guidgenerator.com/online-guid-generator.aspx) for your local app token and secret. Then add the following lines to your settings.cfg:
```
DEBUG=True
TOKEN="your-local-api-token"
SECRET_KEY="your-local-dev-secret"
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
```
Restart the server and go to the home page. Make sure you're viewing the site via your ngrok tunnel. Click the "Get API Token" link in the header. The Google OAuth flow should be working locally.