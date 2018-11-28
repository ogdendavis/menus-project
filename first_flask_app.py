#!/usr/bin/env python

# Simple flask app to learn the framework
from flask import Flask

# Create an instance of Flask, using the application name assigned to this
# module by Python
app = Flask(__name__)

# @app.route tells Flask to execute the following function whenever it receives
# a GET request to the indicated path on the server. This will show the "Hello,
# World! text when a user navigates to the home directory or /hello"
@app.route('/')
@app.route('/hello')
def HelloWorld():
    return 'Hello, World!'

# If module is executed from the Python shell, do this stuff. If it's imported
# into some other code, don't do this stuff!
if __name__ == '__main__':
    # Debug mode makes server reload whenever code change is detected! No need
    # to stop and restart server whenever we want to see a change.
    app.debug = True
    # Serve on all public IP addresses, on port 5000
    app.run(host = '0.0.0.0', port = 5000)
