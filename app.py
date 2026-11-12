import os
import requests
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
app = Flask (__name__)

def envoyer (numero, texte):
   url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
   entetes = {"Authorization": "Bearer " + WHATSAPP_TOKEN}
   corps = {
      "messaging_product": "whatsapp" ,
      "to" : numero,
      "type" : "text",
      "text" :{"body": texte},
   }
   r = requests.post(url, json=corps, headers=entetes)
   print("Envoi :" , r.status_code, r.text)

@app.route("/")
def home():
   return "KAZI Connect est en ligne"

@app.route("/webhook", methods=["GET"])
def verify():
   mode = request.args.get("hub.mode")
   token = request.args.get("hub.verify_token")
   challenge = request.args.get("hub.challenge")
   
   if mode == "subscribe" and token == VERIFY_TOKEN:
      return challenge, 200
   return "Refuse" , 403

sessions = {}
CHOIX_LANGUE = "Choisis ta langue / Chagua lugha / Pona monoko : \n1 Français\n2 Kiswahili\n3 Lingala"
BIENVENUE = {
   "fr": "Langue : français \nBienvenue sur KAZI Connect 👷",
   "sw": "Lugha : Kiswahili \nKaribu kwa KAZI Connect 👷",
   "ln": "Monoko : Lingala \nBoyei malamu na KAZI Connect 👷",
}

TEXTES = {
   "fr": {
      "menu": "Que veux-tu faire ?\n1 Je cherche du travail\n2 Je cherche un travailleur",
      "nom": "Quel est ton nom complet ?",
      "metier": "Quel est ton métier ? (ex : maçon, électricien)",
      "ville": "Dans quelle ville travailles-tu ? (ex : Lubumbashi, Kinshasa)",
      "merci": "✅ Merci {nom} ! Tu es inscrit comme {metier} à {ville}.\nTape menu pour revenir.",
      "menu": "Que veux-tu faire ?\n1 Je cherche du travail\n2 Je cherche un travailleur\n\nTape langue pour changer de langue",
   },
   "sw": {
      "menu": "Unataka kufanya nini?\n1 Natafuta kazi\n2 Natafuta mfanyakazi",
      "nom": "Jina lako kamili ni nani?",
      "metier": "Kazi yako ni ipi? (mf : mjenzi, fundi umeme)",
      "ville": "Unafanya kazi mji gani? (mf : Lubumbashi, Kinshasa)",
      "merci": "✅ Asante {nom}! Umesajiliwa kama {metier} hapa {ville}.\nAndika menu kurudi.",
      "menu": "Unataka kufanya nini?\n1 Natafuta kazi\n2 Natafuta mfanyakazi\n\nAndika lugha kubadilisha lugha",
   },
   "ln": {
      "menu": "Olingi kosala nini?\n1 Nazali koluka mosala\n2 Nazali koluka mosali",
      "nom": "Nkombo na yo ya mobimba nini?",
      "metier": "Mosala na yo nini? (ndakisa : maçon, électricien)",
      "ville": "Ozali kosala na engumba nini? (ex : Lubumbashi, Kinshasa)",
      "merci": "✅ Matondi {nom}! Okomisami lokola {metier} na {ville}.\nKoma menu mpo na kozonga.",
      "menu": "Olingi kosala nini?\n1 Nazali koluka mosala\n2 Nazali koluka mosali\n\nKoma monoko mpo na kobongola monoko",
   },
}


def repondre(numero, texte):
   t = texte.strip().lower()

   if numero not in sessions or t == "menu":
      if numero in sessions and "langue" in sessions[numero] and t == "menu":
         sessions[numero]["etape"] = "menu"
         return TEXTES[sessions[numero]["langue"]]["menu"]
      sessions[numero] = {"etape": "langue"}
      return CHOIX_LANGUE

   if t in ("langue", "lugha", "monoko"):
      sessions[numero]["etape"] = "langue"
      return CHOIX_LANGUE

   session = sessions[numero]
   etape = session["etape"]

   if etape == "langue":
      langues = {"1": "fr", "2": "sw", "3": "ln"}
      if t in langues:
         session["langue"] = langues[t]
         session["etape"] = "menu"
         return TEXTES[session["langue"]]["menu"]
      return CHOIX_LANGUE

   langue = session["langue"]

   if etape == "menu":
      if t == "1":
         session["etape"] = "nom"
         return TEXTES[langue]["nom"]
      return TEXTES[langue]["menu"]

   if etape == "nom":
      session["nom"] = texte.strip()
      session["etape"] = "metier"
      return TEXTES[langue]["metier"]

   if etape == "metier":
      session["metier"] = texte.strip()
      session["etape"] = "ville"
      return TEXTES[langue]["ville"]

   if etape == "ville":
      session["ville"] = texte.strip()
      session["etape"] = "menu"
      return TEXTES[langue]["merci"].format(
         nom=session["nom"], metier=session["metier"], ville=session["ville"])

   return TEXTES[langue]["menu"]
      
@app.route("/webhook", methods=["POST"])
def receive():
   data = request.get_json()
   try :
      value = data["entry"][0]["changes"][0]["value"]
      for m in value.get("messages", []):
         if m.get("type") =="text":
            numero = m["from"]
            texte = m["text"]["body"]
            print("De :", numero, "|message :", texte)
            reponse = repondre(numero, texte)
            print("Réponse :", reponse)
            envoyer(numero, reponse)
            
             
   except Exception as e:
      print("Erreur :", e)
   return "OK", 200
app.run(port=5000)
