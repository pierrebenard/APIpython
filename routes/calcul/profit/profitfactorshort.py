from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

profitfactorshort = Blueprint('profitfactorshort', __name__)

# Connexion à la base de données MongoDB
client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
db = client['test']
collection = db['things']

@profitfactorshort.route('/profitfactorshort', methods=['GET'])
def calculate_profit_factor_short():
    # Calcul du profit total et de la perte totale pour les transactions de type "buy"
    total_profit = 0
    total_loss = 0

    # Parcourir les documents de la collection
    for doc in collection.find({"typeOfTransaction": "sell"}):
        profit = doc['profit']
        if profit > 0:
            total_profit += profit
        elif profit < 0:
            total_loss += profit


    print(f"Total du profit : {total_profit}")
    print(f"Total de la perte : {total_loss}")
    # Calcul du profit factor
    profit_factor = total_profit / abs(total_loss)

    # Insérer le winrate_value dans la collection "unitaire"
    unitaire_collection = db['unitaire']
    unitaire_collection.insert_one({"profitfactorshort": profit_factor})
    unitaire_collection.insert_one({"total_profitshort": total_profit})
    unitaire_collection.insert_one({"total_lossshort": total_loss})

    return jsonify({"profit_factor_short": str(profit_factor)})