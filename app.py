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

def repondre (numero, texte):
   t = texte.strip().lower()
   if numero not in sessions or t == "menu":
      sessions[numero] = {}
      return CHOIX_LANGUE
   langues = {"1" : "fr", "2" : "sw", "3": "ln"}
   if "langues" not in sessions[numero]:
      if t in langues:
         sessions[numero]["langues"] = langues[t]
         return BIENVENUE[langues[t]]
      return CHOIX_LANGUE
   return BIENVENUE[sessions[numero]["langues"]]
      
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
