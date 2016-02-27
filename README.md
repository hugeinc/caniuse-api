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

Setting up VirtualEnvWrapper
---------------------
It is **highly** recommended that you install and use [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html). 
This is the basic how to for Mac OSX. 
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
After cloning your repo and setting up your virtual environment, install the dependencies by running:
```
$ pip install -r requirements.txt
```
There is limited (but growing!) test coverage. To run the tests:
```
$ nosetests
```
After you've installed dependencies and verifed the tests are passing, run:
```
$ python runserver.py
```
And you should see the app running on your [localhost at port 5000](http://localhost:5000)

If you wish to run the HipChat endpoint locally, you'll want to use [ngrok](http://ngrok.com/) to tunnel your localhost to a publicly acessible endpoint for your Integration hook. 
