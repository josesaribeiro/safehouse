import sys
from flask import Flask, json, session, request, abort, redirect, url_for, render_template
from storage import *

app = Flask("Safehouse Server")

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        if 'username' in session:
            username = session['username']
            sensors = getSensorsForUser(username)
            sensorsWrapper = {'sensors': sensors}
            return render_template('index.html', username=username, sensorsWrapper=sensorsWrapper)
        else:
            return redirect(url_for('login'))

# User login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return '''
            <h1>Log in with your username and password</h1>
            <form action="/login" method="post">
                <p>Username <input type=text name=username>
                <p>Password <input type=text name=hashedPassword>
                <p><input type=submit value=Login>
            </form>
            <a href="register">Don't have a username? Sign up now!</a>
        '''
    elif request.method == 'POST':
        username = request.form['username']
        hashedPassword = request.form['hashedPassword']
        if verifyUser(username, hashedPassword):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

# User registration
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return '''
            <h1>Sign up for Safehouse</h1>
            <form action="/register" method="post">
                <p>Username <input type=text name=username>
                <p>Password <input type=text name=hashedPassword0>
                <p>Re-enter password <input type=text name=hashedPassword1>
                <p><input type=submit value=Register>
            </form>
            <a href="login">Know your username? Log in here!</a>
        '''
    elif request.method == 'POST':
        username = request.form['username']
        hashedPassword0 = request.form['hashedPassword0']
        hashedPassword1 = request.form['hashedPassword1']
        if hashedPassword0 == hashedPassword1:
            if addUser(username, hashedPassword0) is not None:
                session['username'] = username
                return redirect(url_for('index'))
        return redirect(url_for('register'))

# User logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

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
    print '(sensorID: %s, status: %i)' % (sensorID, status)
    updateSensorStatus(sensorID, status)
    return 'Update succeeded'

# Get sensor information
@app.route('/get-sensors', methods=['GET'])
def getSensors():
    if 'username' in session:
        return json.dumps(getSensorsForUser(session['username']))
    else:
        return redirect(url_for('login'))

# Register sensor to the logged in user
@app.route('/register-sensor-to-user', methods=['POST'])
def registerSensorToUser():
    if 'username' in session:
        sensorID = request.form['sensorID']
        description = request.form['description']
        username = session['username']
        if addSensorUser(sensorID, username, description) is not None:
            print username + ' has successfully added' + sensorID + '.\n'
        else:
            print username + ' tried to add ' + sensorID + ' but failed.\n'
        return redirect(url_for('getSensors'))
    else:
        return redirect(url_for('login'))

app.secret_key = '\x8a\xf2\xaa8\xe1\xac%m\x1bw\x88D%!\x89=Q2\x00QrE}4'

if __name__ == '__main__':
    app.run(debug=False,
    	host=app.config.get("HOST", "0.0.0.0"),
    	port=app.config.get("PORT", 9000))

