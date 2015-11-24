import sys
from flask import Flask, json, session, request, abort, redirect, url_for, render_template
from storage import *

app = Flask("Safehouse Server")

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('profile'))
        else:
            return render_template('index.html')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if request.method == 'GET':
        if 'username' in session:
            username = session['username']
            sensors = getSensorsForUser(username)
            sensorsWrapper = {'sensors': sensors}
            return render_template('profile.html', username=username, sensorsWrapper=sensorsWrapper)
        else:
            return redirect(url_for('login'))

# User login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('profile'))
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        hashedPassword = request.form['hashedPassword']
        if verifyUser(username, hashedPassword):
            session['username'] = username
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('login'))

# User registration
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('profile'))
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['username']
        hashedPassword0 = request.form['hashedPassword0']
        hashedPassword1 = request.form['hashedPassword1']
        if hashedPassword0 == hashedPassword1:
            if addUser(username, hashedPassword0) is not None:
                session['username'] = username
                return redirect(url_for('profile'))
        return redirect(url_for('register'))

# User logout
@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('index'))

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
    status = int(request.form['status'])
    updateSensorStatus(sensorID, status)
    return 'Update succeeded'

# Get sensor information
@app.route('/get-sensors', methods=['GET'])
def getSensors():
    if 'username' in session:
        return json.dumps({"sensors": getSensorsForUser(session['username'])})
    else:
        return redirect(url_for('login'))

# Get sensor information
@app.route('/get-sensors-ryan', methods=['GET'])
def getSensorsRyan():
    return json.dumps({"sensors": getSensorsForUser('Ryan')})

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
    return redirect(url_for('profile'))

@app.route('/remove-sensor-from-user', methods=['POST'])
def removeSensorFromUser():
    if 'username' in session:
        sensorID = request.form['sensorID']
        username = session['username']
        deleteSensorUser(sensorID, username)
    return redirect(url_for('profile'))

app.secret_key = '\x8a\xf2\xaa8\xe1\xac%m\x1bw\x88D%!\x89=Q2\x00QrE}4'

if __name__ == '__main__':
    app.run(debug=False,
    	host=app.config.get("HOST", "0.0.0.0"),
    	port=app.config.get("PORT", 9000))

