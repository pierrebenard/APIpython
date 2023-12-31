from flask import Flask, Blueprint, jsonify
from pymongo import MongoClient

average_rr = Blueprint('average_rr', __name__)

client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority')
db = client['test']


@average_rr.route('/average_rr', methods=['GET'])
def calculate_average_rr(data):
    username = data.get('username')
    collection_name = f"{username}_close"
    collection_unitaire = f"{username}_unitaire"
    collection = db[collection_name]
    rr_values = []
    for document in collection.find():
        if "RR" in document:
            rr_values.append(document["RR"])

    print("Valeurs de RR dans la collection 'things':", rr_values)

    rr_total = sum(rr_values)
    rr_count = len(rr_values)
    average_rr = rr_total / rr_count if rr_count > 0 else 0

    unitaire_collection = db[collection_unitaire]
    unitaire_collection.update_one({}, {"$set": {"RRaverage": average_rr}}, upsert=True)


