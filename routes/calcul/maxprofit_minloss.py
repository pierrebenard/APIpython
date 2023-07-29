from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

maxprofit_minloss = Blueprint('maxprofit_minloss', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']


@maxprofit_minloss.route('/maxprofit_minloss', methods=['GET'])
def find_max_profit_and_min_loss(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    # Initialisation des variables
    max_profit_value = float('-inf')  # Valeur initiale de profit maximale
    min_loss_value = float('inf')  # Valeur initiale de perte minimale

    # Parcourir les documents de la collection
    for doc in collection.find():
        profit = doc['profit']

        # Recherche du profit maximum
        if profit > max_profit_value:
            max_profit_value = profit

        # Recherche de la perte minimale
        if profit < min_loss_value:
            min_loss_value = profit

    # Insérer les valeurs dans la collection "unitaire"
    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one(
        {},
        {'$set': {'Max profit2': max_profit_value, 'Max loss2': min_loss_value}},
        upsert=True
    )