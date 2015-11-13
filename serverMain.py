import json
import sys
from flask import Flask, request, abort, redirect, url_for

app = Flask("Safehouse Server")

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'GET':
    	return 'Welcome to the Safehouse Server!'
    elif request.method == 'POST':
    	jsonObject = request.get_json()
    	print json.dumps(jsonObject)
    	return json.dumps(jsonObject)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return 'This is a registration page. Please post with the following \
                schema: \
                {"username": <string>, "hashedPassword": <string>} \
                Choose your own hashing algorithm for the password, as long \
                as it is the same one used during user login.'
    elif request.method == 'POST':
        # check that username is unique (against the Users collection) and
        # create the user
        return 'Unimplemented'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return 'This is a login page. Please post with the following schema: \
                {"username": <string>, "hashedPassword": <string>} \
                Choose your own hashing algorithm for the password, as long \
                as it is the same one used during user registration.'
    elif request.method == 'POST':
        # verify credentials against Users collection, then log in the user
        return 'Unimplemented'

@app.route('/location', methods=['POST', 'GET'])
def location():
    if request.method == 'GET':
        return 'Update the user\'s location here. Please post with the \
                following schema: \
                {"lattitude": <float>, "longitude": <float>}'
    elif request.method == 'POST':
        # update location for user
        return 'Unimplemented'

if __name__ == '__main__':
    app.run(debug=False,
    	host=app.config.get("HOST", "0.0.0.0"),
    	port=app.config.get("PORT", 9000))

