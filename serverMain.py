import sys
from flask import Flask, json, session, request, abort, redirect, url_for
from storage import *

app = Flask("Safehouse Server")

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        if 'username' in session:
            return 'Logged in as ' + session['username']
        else:
            return redirect(url_for('login'))

# User login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return '''
            <form action="/login" method="post">
                <p>Username <input type=text name=username>
                <p>Password <input type=text name=hashedPassword>
                <p><input type=submit value=Login>
            </form>
        '''
    elif request.method == 'POST':
        username = request.form['username']
        hashedPassword = request.form['hashedPassword']
        if verifyUser(username, hashedPassword):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

# User logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# User registration
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

@app.route('/location', methods=['POST', 'GET'])
def location():
    if request.method == 'GET':
        return 'Update the user\'s location here. Please post with the \
                following schema: \
                {"lattitude": <float>, "longitude": <float>}'
    elif request.method == 'POST':
        # update location for user
        return 'Unimplemented'

# Sensor posts
@app.route('/update-sensor', methods=['POST'])
def updateSensor():
    sensorID = request.form['sensorID']
    status = request.form['status']
    print 'sensorID: ' + sensorID + '\n'
    print 'status: ' + status + '\n'
    updateSensorStatus(sensorID, status)
    return 'Update succeeded'

app.secret_key = '\x8a\xf2\xaa8\xe1\xac%m\x1bw\x88D%!\x89=Q2\x00QrE}4'

if __name__ == '__main__':
    app.run(debug=False,
    	host=app.config.get("HOST", "0.0.0.0"),
    	port=app.config.get("PORT", 9000))

