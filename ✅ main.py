import requests
from bs4 import BeautifulSoup
import time

# === Paramètres ===
URL = "https://www.parisversailles.com/inscription_bourse.php"
PUSHBULLET_API_KEY = "o.OH9iiXMk3Mcf301K1Hj3WHmqKPINqK55"  # Ton token personnel

def send_pushbullet_notification(title, body):
    data = {
        "type": "note",
        "title": title,
        "body": body
    }
    headers = {
        "Access-Token": PUSHBULLET_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post("https://api.pushbullet.com/v2/pushes", json=data, headers=headers)
    if response.status_code != 200:
        print("Erreur lors de l'envoi de la notification :", response.text)
    else:
        print("Notification envoyée avec succès.")

def check_dossards():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table")
    if not table:
        print("Pas de tableau trouvé.")
        return False

    rows = table.find_all("tr")[1:]  # ignorer l'en-tête
    if rows:
        print(f"{len(rows)} dossards trouvés.")
        message = "\n".join(
            " | ".join(cell.text.strip() for cell in row.find_all("td")) for row in rows
        )
        send_pushbullet_notification("🎽 Dossards disponibles !", message)
        return True
    else:
        print("Aucun dossard pour le moment.")
        return False

# === Boucle infinie ===
while True:
    print("Vérification des dossards...")
    found = check_dossards()
    print("Attente de 5 minutes...\n")
    time.sleep(300)
