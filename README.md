# BadgerBibEngine: https://badger-bib-engine.herokuapp.com/
A simple web-based database application for searching, uploading, and deleting bibliometric data! You can use the application at https://badger-bib-engine.herokuapp.com/. 

We are currently hosting the application and our MySQL database on Heroku's free tier and have thus maxed out our alotted DB space. This means creating new user accounts and using the edit interface is not available online. Feel free to use,

username: <b>Peter</b>
password: <b>Bryant</b>

in order to sign in, alternatively just continue as guest. A demo video of the application running locally can be found in the documentation page once logged in!

<h4>Running BadgerBibEngine Locally</h4>

<p>Clone my repository</p>

```python
$ git clone https://github.com/peter-w-bryant/BadgerBibEngine.git
```
<p>Create + activate virtual environment</p>

```python
$ python3 -m venv ./env
$ env/Scripts/activate
```
<p>Install all dependencies</p>

```python
$ pip3 install -r requirements.txt
```

<p>Run the app and start your local server</p>

```python
$ python3 app.py
```
