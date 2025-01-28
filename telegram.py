import telebot
import cv2
import operator
import os

# Initialisation du bot Telegram
bot = telebot.TeleBot("your_key")

# Répertoire où stocker les images
DATA_DIR = "data"

# Vérifier si le répertoire existe, sinon le créer
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Initialisation des classificateurs en cascade pour la détection de visages
face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt2.xml")
profile_cascade = cv2.CascadeClassifier("./haarcascade_profileface.xml")

# Fonction de détection de visages
def detect_faces(frame):
    tab_face = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Détection de visages frontaux
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4, minSize=(5, 5))
    for (x, y, w, h) in faces:
        tab_face.append([x, y, x+w, y+h])
    # Détection de visages de profil
    profile_faces = profile_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=4)
    for (x, y, w, h) in profile_faces:
        tab_face.append([x, y, x+w, y+h])
    return tab_face

# Gestionnaire de commandes '/start' et '/help'
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bonjour ! Envoyez-moi une photo et je détecterai les visages.")

# Gestionnaire pour les photos envoyées par les utilisateurs
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Récupérer les informations sur la photo
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    # Enregistrer la photo dans le répertoire "data"
    file_path = os.path.join(DATA_DIR, f"{message.photo[-1].file_id}.jpg")
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    # Charger la photo pour la détection de visages
    img = cv2.imread(file_path)
    tab_faces = detect_faces(img)
    # Dessiner des rectangles autour de tous les visages détectés
    for (x, y, x2, y2) in tab_faces:
        cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)
    # Enregistrer l'image avec les rectangles dessinés
    cv2.imwrite(file_path, img)
    # Envoyer l'image modifiée à l'utilisateur
    bot.send_photo(message.chat.id, open(file_path, 'rb'))

@bot.message_handler(commands=['linkedin'])
def send_linkedin_profile(message):
    bot.send_message(message.chat.id, "Voici mon profil LinkedIn :(https://www.linkedin.com/in/saifeddine-mabrouk-555816198/)", parse_mode='Markdown')

    
@bot.message_handler(func=lambda message: True)
def handle_other(message):
    bot.reply_to(message, "Veuillez envoyer une photo, s'il vous plaît.")
# Gestionnaire pour le bouton "Soutenir"



# Démarrage du bot
bot.polling()
