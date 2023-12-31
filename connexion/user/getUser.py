from flask import Blueprint, jsonify
from pymongo import MongoClient

def setup_user_routes(app):
    # Connexion à la base de données MongoDB
    mongo_client = MongoClient('mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority')
    db = mongo_client['test']
    users_collection = db['users']

    user_blueprint = Blueprint('user', __name__)

    @user_blueprint.route('/users/<string:user_id>', methods=['GET'])
    def get_user(user_id):
        result = _get_user(user_id)

        return jsonify(result["data"]), result["status"]

    def _get_user(user_id):
        try:
            user = users_collection.find_one({"_id": user_id})

            if user is None:
                return {"status": 404, "data": {"message": "Utilisateur non trouvé"}}

            return {"status": 200, "data": {"user": user}}

        except Exception as e:
            return {"status": 500, "data": {"error": str(e)}}

    return user_blueprint
