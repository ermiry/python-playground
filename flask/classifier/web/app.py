from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import requests
import subprocess
import json

app = Flask (__name__)
api = Api (app)

# connect to mongo
client = MongoClient ("mongodb://db:27017")
db = client.ImageRecognition	# create a new db
users = db["Users"]		# create a new collection inside the db

# check if the user exists in the db or not
def UserExist (username):
	if users.find ({ "Username": username }).count () == 0:
		return False

	else: 
		return True

class Register (Resource):
	def post (self):
		postedData = request.get_json ()

		username = postedData["username"]
		password = postedData["password"]

		if UserExist (username):
			retjson = {
				"status": 301,
				"msg": "Invalid username"
			}

			return jsonify (retjson);

		hashed_pwd = bcrypt.hashpw (password.encode("utf8"), bcrypt.gensalt ())

		# store the user into the db
		users.insert ({
			"Username": username,
			"Password": hashed_pwd,
			"Tokens": 4
		})

		retjson = {
			"status": 200,
			"msg": "success"
		}

		return jsonify (retjson)