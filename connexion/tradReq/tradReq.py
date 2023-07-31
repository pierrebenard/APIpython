from flask import Flask, Blueprint, jsonify, request
from pymongo import MongoClient
import bcrypt
from datetime import time
from routes.calcul.TPR import calculate_tpr
from routes.calcul.SLR import calculate_slr
from routes.calcul.killzone import calculate_killzone
from routes.calcul.session import determine_session
from routes.calcul.calculate_duration import calculate_time_duration
from routes.calcul.RR import calculate_rr
from routes.calcul.RRT import calculate_rrt
from routes.calcul.Equity import calculate_equity
from routes.calcul.weekday import add_weekday


#code groupé

from routes.calcul.max_successive_counts import find_max_successive_counts # code groupé max successive gain et max successive loss
from routes.calcul.maxprofit_minloss import find_max_profit_and_min_loss # code groupé max profit max loss
from routes.calcul.profit.profitfactorgroup import calculate_profit_factor_group
from routes.calcul.winrategroup import calculate_winrate_group
from routes.calcul.average.averagegainloss import calculate_average_gain_loss_rr
from routes.calcul.winrrtflat import calculate_winrrtflat
from routes.calcul.sharp import calculate_sharp_ratio

#from routes.calcul.profit.profitfactor  import calculate_profit_factor // remplacé par le code groupé profit_factor_group
#from routes.calcul.profit.profitfactorlong  import calculate_profit_factor_long  // remplacé par le code groupé profit_factor_group
#from routes.calcul.profit.profitfactorshort  import calculate_profit_factor_short  // remplacé par le code groupé profit_factor_group
#from routes.calcul.minloss  import find_min_loss // remplacé par le code groupé maxprofit_minloss
#from routes.calcul.maxprofit  import find_max_profit // remplacé par le code groupé maxprofit_minloss
#from routes.calcul.max_successive_gain import find_max_successive_gains // remplacé par code groupé max_successive_count
#from routes.calcul.max_successive_losses import find_max_successive_losses // remplacé par code groupé max_successive_count
#from routes.calcul.winrate import calculate_winrate // remplacé par le code winrategroup
#from routes.calcul.winratestd  import calculate_winratestd // remplacé par le code winrategroup
#from routes.calcul.average.averagegain import calculate_average_gain // remplace par averagegainloss
#from routes.calcul.average.averageloss import calculate_average_loss // remplace par averagegainloss
#from routes.calcul.average.average_rr import calculate_average_rr // remplace par averagegainloss
#from routes.calcul.average.average_duration import calculate_average_duration // remplace par le code averagegainloss
#from routes.calcul.ddmax import calculate_ddmax // remplacé par le code maxprofit_minloss

# Connexion à la base de données MongoDB
client = MongoClient("mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/test?retryWrites=true&w=majority")
db = client["test"]

app = Flask(__name__)

# Trade Blueprint
trade_blueprint = Blueprint('trade', __name__)
SLOpen = {}
def compare_passwords(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

@trade_blueprint.route('/savetraderequest', methods=['POST'])
def save_trade_request():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    closure_position = data.get('closurePosition')

    try:
        user = db.users.find_one({"username": username})
        if not user or not compare_passwords(password, user['password']):
            return jsonify({"message": "Access denied"}), 401

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        collection_name = f"{username}_open" if closure_position == "Open" else f"{username}_close"

        user_collection = db[collection_name]
        if  closure_position == "":
            volume_remain = data.get('volume')
            if volume_remain < 0.01:
                volume_remain = 0
                user_collection.delete_one({"identifier": data.get('identifier')})
            
        
        if closure_position == "Open" :
            volume_remain = data.get('volume')
            if volume_remain < 0.01:
                volume_remain = 0
                user_collection.delete_one({"identifier": data.get('identifier')})
            SLOpen[data.get('identifier')] = data.get('stopLoss')
        else:
            # Check if there's a corresponding 'Open' order with the same identifier
            open_orders = db[f"{username}_open"]
            open_order = open_orders.find_one({"identifier": data.get('identifier')})
            if open_order:
                volume_remain = open_order.get('volume_remain', 0) - data.get('volume')
                if volume_remain < 0:
                    volume_remain = 0
                open_orders.update_one({"identifier": data.get('identifier')}, {"$set": {"volume_remain": volume_remain}})
                if volume_remain == 0:
                    open_orders.delete_one({"identifier": data.get('identifier')})
            else:
                return jsonify({"message": "No corresponding 'Open' order found"}), 400
           
        

        # Remove 'volume_remain' field for 'Close' orders
        if closure_position == "Close":
            data.pop("volume_remain", None)

            # Calculate SLR only for 'Close' orders
            slr_value = calculate_slr(data)
            data['SLR'] = slr_value['SLR']
            

            # Calculate TPR only for 'Close' orders
            tpr_value = calculate_tpr(data)
            data['TPR'] = tpr_value['TPR']
            
            
            killzone = calculate_killzone(data)
            data['killzone'] = killzone
            
            session = determine_session(data)
            data['session'] = session
            
            duration = calculate_time_duration(data)
            data['duration'] = duration['duration']
            
            rr = calculate_rr(data)
            data['RR'] = rr
            
            rrt = calculate_rrt(data)
            data['RRT'] = rrt
            
            equity = calculate_equity(data)
            data['Equity'] = equity
            
            weekday_str = add_weekday(data)
            data['Day'] = weekday_str

       
                       

          

        # Round 'volume' and 'volume_remain' to two decimal places
        data['volume'] = round(data.get('volume'), 2)
        volume_remain = round(volume_remain, 2)

        # Calculate killzone only for 'Open' orders
        if closure_position == "Open":
            killzone = calculate_killzone(data)
            data['killzone'] = killzone

            session = determine_session(data)
            data['session'] = session

            rrt = calculate_rrt(data)
            data['RRT'] = rrt

            weekday_str = add_weekday(data)
            data['Day'] = weekday_str

            
            
        # Insert the data into the collection
        #user_collection.insert_one(data)

        trade_request = {
            "username": username,
            "password": hashed_password,
            "ticketNumber": data.get('ticketNumber'),
            "identifier": data.get('identifier'),
            "magicNumber": data.get('magicNumber'),
            "dateAndTimeOpening": data.get('dateAndTimeOpening'),
            "typeOfTransaction": data.get('typeOfTransaction'),
            "orderType": data.get('orderType'),
            "volume": data.get('volume'),
            "volume_remain": volume_remain,
            "symbol": data.get('symbole'),
            "priceOpening": data.get('priceOpening'),
            "stopLoss": data.get('stopLoss'),
            "SLOpen" : SLOpen.get(data.get('identifier')),
            "takeProfit": data.get('takeProfit'),
            "dateAndTimeClosure": data.get('dateAndTimeClosure'),
            "priceClosure": data.get('priceClosure'),
            "swap": data.get('swap'),
            "profit": data.get('profit'),
            "commission": data.get('commision'),
            "closurePosition": data.get('closurePosition'),
            "balance": data.get('balance'),
            "broker": data.get('broker'),
            "annonceEconomique": None,
            "psychologie": None,
            "strategie": None,
            "position": None,
            "typeOrdre": None,
            "violeStrategie": None,
            "sortie": None,
            "killzone": data.get("killzone"),
            "session": data.get("session"),
            "duration": data.get('duration'),
            "TPR": data.get('TPR'),
            "SLR": data.get('SLR'),
            "RR": data.get('RR'),
            "RRT": data.get('RRT'),
            "Equity": data.get('Equity'),
            "Day": data.get('Day'),           
            "strategie": None,
            "timeEntree": None,
            "timeSetup": None,
            "sortieManuelle": None,
            "journeeDeTilt": None,
            "TJS": None
        }
        #combined_data = [trade_request, data]
        # Insertion des données dans la collection
        user_collection.insert_one(trade_request)
      
     
        find_max_successive_counts(data)
        find_max_profit_and_min_loss(data)
        calculate_profit_factor_group(data)
        calculate_winrate_group(data)
        calculate_average_gain_loss_rr(data) 
        calculate_winrrtflat(data)
        calculate_sharp_ratio(data)
             
        #calculate_profit_factor(data)  // remplacé par le code groupé profit_factor_group        
        #calculate_profit_factor_long(data)   // remplacé par le code groupé profit_factor_group            
        #calculate_profit_factor_short(data)  // remplacé par le code groupé profit_factor_group           
        #find_min_loss(data)   // remplacé par le code groupé maxprofit_minloss            
        #find_max_profit(data)  // remplacé par le code groupé maxprofit_minloss
        #find_max_successive_gains(data) // remplacé par code groupé max_successive_count          
        #find_max_successive_losses(data) // remplacé par code groupé max_successive_count
        #calculate_winrate(data) // remplacé par le code winrategroup           
        #calculate_winratestd(data) // remplacé par le code winrategroup
        #calculate_average_gain(data)  // remplace par averagegainloss
        #calculate_average_loss(data) // remplace par averagegainloss 
        #calculate_average_rr(data) // remplace par averagegainloss
        #calculate_average_duration(data) // remplace par le code averagegainloss
        #calculate_ddmax(data)  // remplacé par le code maxprofit_minloss
        
        return jsonify({"message": "Data saved successfully with TPR and SLR kill"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Enregistrement du blueprint "trade" dans l'application Flask
app.register_blueprint(trade_blueprint, url_prefix='/api')


if __name__ == '__main__':
    app.run()
