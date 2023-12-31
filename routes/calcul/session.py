from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient
from datetime import datetime, time

session = Blueprint('session', __name__)


def determine_session(data):
    opening_time = datetime.strptime(data['dateAndTimeOpening'], "%Y-%m-%dT%H:%M:%S.%f%z")
    if time(0, 0) <= opening_time.time() < time(7, 0):
        session_value = "AS"
    elif time(8, 0) <= opening_time.time() < time(12, 0):
        session_value = "LD"
    elif time(13, 0) <= opening_time.time() < time(15, 0):
        session_value = "NY"
    else:
        session_value = "ND"

    return session_value


