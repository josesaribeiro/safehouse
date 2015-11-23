# Script for initializing our MongoDB database, specifying data schemas, and
# providing data access helper functions

from pymongo import MongoClient
from const import *

database = MongoClient(
	"mongodb://username:password@ds053954.mongolab.com:53954/sandbox"
).sandbox

# User
# {
# 	"username": <string>,
# 	"hashedPassword": <string>
# }
# Primary key: (username)
userCollection = database['User']

# Sensor
# {
# 	"sensorID": <string>,
# 	"sensorType": <string>,
# 	"status": <string>
# }
# Primary key: (sensorID)
sensorCollection = database['Sensor']

# SensorUser
# A user  can oversee multiple sensors, and multiple users can oversee
# the same sensor.
# {
# 	"sensorID": <string>,
# 	"username": <string>,
#   "description": <string>
# }
# Primary key: (sensorID, username)
sensorUserCollection = database['SensorUser']



# get the (username, hashedPassword) pair for a given username
def getUser(username):
	return userCollection.find_one({
		"username": username
	})

# verifies the (username, hashedPassword) pair against the User collection
def verifyUser(username, hashedPassword):
	return userCollection.find_one({
		"username": username,
		"hashedPassword": hashedPassword
	}) is not None

# returns object ID if added correctly, returns None otherwise
def addUser(username, hashedPassword):
	if getUser(username) is None:
		return userCollection.insert_one({
			"username": username,
			"hashedPassword": hashedPassword
		}).inserted_id
	else:
		return None

# adds or updates the location of a user
def setLocation(username, lattitude, longitude):
	newLocation = {
		"lattitude": lattitude,
		"longitude": longitude
	}
	return userCollection.update_one(
		{ "username": username },
		{ '$set': { "location": newLocation } },
		upsert = True
	).upserted_id

# get sensor information for a given sensor ID
def getSensor(sensorID):
	return sensorCollection.find_one({
		"sensorID": sensorID
	})

# returns object ID if added correctly, return None otherwise
def addSensor(sensorID, sensorType):
	if getSensor(sensorID) is None:
		return sensorCollection.insert_one({
			"sensorID": sensorID,
			"sensorType": sensorType,
			"status": STATUS_TRIGGERED
		}).inserted_id
	else:
		return None

# update sensor status
def updateSensorStatus(sensorID, status):
	return sensorCollection.update_one(
		{ "sensorID": sensorID },
		{ '$set': { "status": status } },
		upsert = True
	).upserted_id

# determines if a given user uses a given sensor
def isSensorUser(sensorID, username):
	return sensorUserCollection.find_one({
		"sensorID": sensorID,
		"username": username
	}) is not None

# returns object ID if added correctly, return None otherwise
def addSensorUser(sensorID, username, description):
	print "began addsensoruser function"
	if isSensorUser(sensorID, username) == False:
		if getUser(username) is not None:
			if getSensor(sensorID) is not None:
				return sensorUserCollection.insert_one({
					"sensorID": sensorID,
					"username": username,
					"description": description
				})
	return None

# returns all sensors belonging to 'username'
def getSensorsForUser(username):
	returnList = []
	for sensorAndUserInfo in sensorUserCollection.find({"username": username}):
		sensorQueryResult = sensorCollection.find_one({
			"sensorID": sensorAndUserInfo['sensorID']
		})
		sensorObjectToReturn = {
			"id": sensorQueryResult['sensorID'],
			"type": sensorQueryResult['sensorType'],
			"description": sensorAndUserInfo['description'],
			"status": sensorQueryResult['status']
		}
		returnList.append(sensorObjectToReturn)
	return returnList



