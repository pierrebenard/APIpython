import sys
from webbrowser import register
from pymongo import MongoClient
import requests
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

"""
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content, Accept, Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, PATCH, OPTIONS'
    return response

app.after_request(after_request)
"""


app.debug = False
CORS(app, resources={r"*": {"origins": "*"}})

# indicateur
from connexion.indicateur.createIndicateur import createIndicateur
from connexion.indicateur.recuperationIndicateur import recuperationIndicateur
from connexion.indicateur.suppressionIndicateur import suppressionIndicateur

# porteFeuille
from connexion.portefeuille.createPortefeuille import createPorteFeuille
from connexion.portefeuille.suppressionPortefeuille import suppressionPorteFeuille
from connexion.portefeuille.recuperationPortefeuille import recuperationPorteFeuille

# strategie
from connexion.strategie.createStrategie import createStrategie
from connexion.strategie.recuperationStrategie import recuperationStrategie
from connexion.strategie.suppressionStrategie import suppressionStrategie

# recuperation trade de mt5
from connexion.tradReq.tradReq import trade_blueprint

# user
from connexion.user.getUser import setup_user_routes
from connexion.user.login import setup_login_routes
from connexion.user.signup import setup_signup_route

# calcul
from routes.calcul.assign_order import assign_order

#from routes.calcul.BE_RR.RR import RR
#from routes.calcul.BE_RR.BE import BE
from routes.calcul.calculate_duration import calculate_duration

from routes.calcul.Equity import Equity
from routes.calcul.killzone import killzone

from routes.calcul.session import session

from routes.calcul.SLR import slr
from routes.calcul.Tilts import Tilts
from routes.calcul.TPR import tpr
#from routes.calcul.tradecount import tradecount
from routes.calcul.weekday import weekday

#from routes.calcul.conversion_map import conversion_map
from routes.calcul.RR import RR
from routes.calcul.RRT import RRT
from routes.calcul.max_successive_counts import max_successive_counts #code groupé max successive gain et loss
from routes.calcul.maxprofit_minloss import maxprofit_minloss #code groupé max gain et max loss
from routes.calcul.profit.profitfactorgroup import profitfactorgroup
from routes.calcul.winrategroup import winrategroup
from routes.calcul.average.averagegainloss import averagegainloss 
from routes.calcul.winrrtflat import winrrtflat
from routes.calcul.tradercount import tradercount
from routes.calcul.BE import BE
from routes.calcul.limit import limit
from routes.calcul.bestrr import bestrr



#from routes.calcul.maxprofit import maxprofit // remplacé par le code groupé maxprofit_minloss
#from routes.calcul.minloss import minloss // remplacé par le code groupé maxprofit_minloss
#from routes.calcul.profit.profitfactor import profitfactor // remplacé par le code groupé profit_factor_group
#from routes.calcul.profit.profitfactorlong import profitfactorlong // remplacé par le code groupé profit_factor_group
#from routes.calcul.profit.profitfactorshort import profitfactorshort // remplacé par le code groupé profit_factor_group
#from routes.calcul.winrate import winrate // remplacé par winrategroup
#from routes.calcul.winratestd import winratestd // remplacé par winrategroup
#from routes.calcul.ddmax import ddmax // remplacé par le code maxprofit_minloss
#from routes.calcul.average.average_duration import average_duration // remplacé par le code groupe averagegainloss
#from routes.calcul.average.average_rr import average_rr // remplacé par le code groupe averagegainloss
#from routes.calcul.average.averagegain import averagegain // remplacé par le code groupe averagegainloss
#from routes.calcul.average.averageloss import averageloss  // remplacé par le code groupe averagegainloss
#from routes.calcul.sharp import sharp //groupé avec maxgain_minloss

# envoie
from routes.envoie.envoie import envoie

# image
from routes.journal.enregistrementImage import enregistrerImage
from routes.journal.recuperationImage import recuperationImage

#journal
from routes.journal.modificationTrade import setup_modificationTrade_routes
from routes.journal.recuperationTrade import setup_things_routes


#===========================================INITIALISATION DU SERVEUR TERMINE===============================================#


app.register_blueprint(tpr)
app.register_blueprint(assign_order)
app.register_blueprint(BE)
app.register_blueprint(RR)
app.register_blueprint(RRT)
app.register_blueprint(calculate_duration)

app.register_blueprint(Equity)
app.register_blueprint(killzone)
app.register_blueprint(session)

app.register_blueprint(slr)
app.register_blueprint(Tilts)
app.register_blueprint(tpr)
#app.register_blueprint(tradecount)
app.register_blueprint(weekday)
app.register_blueprint(envoie)
app.register_blueprint(max_successive_counts)
app.register_blueprint(maxprofit_minloss)
app.register_blueprint(profitfactorgroup)
app.register_blueprint(winrategroup)
app.register_blueprint(averagegainloss)
app.register_blueprint(winrrtflat)
app.register_blueprint(tradercount)
app.register_blueprint(limit)
app.register_blueprint(bestrr)
#app.register_blueprint(sharp) //groupé avec maxgain_minloss
#app.register_blueprint(maxprofit) // remplacé par le code groupé maxprofit_minloss
#app.register_blueprint(minloss) // remplacé par le code groupé maxprofit_minloss
#app.register_blueprint(profitfactor) // remplacé par le code groupé profit_factor_group
#app.register_blueprint(profitfactorlong) // remplacé par le code groupé profit_factor_group
#app.register_blueprint(profitfactorshort) // remplacé par le code groupé profit_factor_group
#app.register_blueprint(average_duration)
#app.register_blueprint(average_rr)
#app.register_blueprint(averagegain)
#app.register_blueprint(averageloss)
#app.register_blueprint(winratestd)
#app.register_blueprint(winrate)
#app.register_blueprint(conversion_map)
#app.register_blueprint(ddmax)

# user
app.register_blueprint(setup_signup_route(app))
app.register_blueprint(setup_login_routes(app))
app.register_blueprint(setup_user_routes(app))

# recuperation trade de mt5
app.register_blueprint(trade_blueprint)

# strategie
app.register_blueprint(recuperationStrategie)
app.register_blueprint(createStrategie)
app.register_blueprint(suppressionStrategie)

# porteFeuille
app.register_blueprint(recuperationPorteFeuille)
app.register_blueprint(createPorteFeuille)
app.register_blueprint(suppressionPorteFeuille)

# indicateur
app.register_blueprint(recuperationIndicateur)
app.register_blueprint(createIndicateur)
app.register_blueprint(suppressionIndicateur)

# envoie
app.register_blueprint(envoie)

# journal
app.register_blueprint(setup_things_routes(app))
app.register_blueprint(setup_modificationTrade_routes(app))

# image
app.register_blueprint(enregistrerImage)
app.register_blueprint(recuperationImage)

#===========================================LANCEMENT DU SERVER===============================================#
if __name__ == '__main__':
    url = "mongodb+srv://pierre:ztxiGZypi6BGDMSY@atlascluster.sbpp5xm.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(url, connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
    collection = client.db["things"]
    app.run(host='0.0.0.0', port=1234)
