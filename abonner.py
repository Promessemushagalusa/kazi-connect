import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("WHATSAPP_TOKEN")
waba = "1067440542784028"
url = f"https://graph.facebook.com/v21.0/{waba}/subscribed_apps"
entetes = {"Authorization": "Bearer " + token}

print("Avant :", requests.get(url, headers=entetes).text)
print("Abonnement :", requests.post(url, headers=entetes).text)