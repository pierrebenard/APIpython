from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']

# Blueprint pour /sortiemanu
sortiemanu = Blueprint('sortiemanu', __name__)

@sortiemanu.route('/sortiemanu', methods=['GET'])
def calculate_sortiemanu(data):


    username = data.get('username')
    collection_name = f"{username}_close"
    collection = db[collection_name]
    
    closurePosition = data.get('closurePosition')
    TPR = data.get('TPR')
    SLR = data.get('SLR')

    if closurePosition == 'Close' and TPR == false and SLR == false:
        Smanu = true
    else:
        Smanu = false

    return jsonify({'Smanu': Smanu})





