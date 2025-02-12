import os
import pytesseract # type: ignore
import cv2
import numpy as np
import sqlite3
from PIL import Image

# Configura il percorso di Tesseract se necessario
pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"  # Modifica in base al sistema operativo

# Percorsi
DB_FILE = "images.db"
IMG_FOLDER = "screenshots"

# Crea o connette al database SQLite
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT UNIQUE,
        text TEXT
    )
""")
conn.commit()

def preprocess_image(image_path):
    """ Applica miglioramenti all'immagine per un OCR più accurato """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Converti in scala di grigi

    # Rimozione del rumore e miglioramento del contrasto
    img = cv2.bilateralFilter(img, 9, 75, 75)  # Riduce il rumore preservando i bordi

    # Thresholding (binarizzazione)
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Ridimensionamento per migliorare il riconoscimento OCR
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Salva immagine temporanea
    temp_path = "temp.png"
    cv2.imwrite(temp_path, img)
    return temp_path

def extract_text_from_image(image_path):
    """ Estrae testo ottimizzato da un'immagine con OCR avanzato """
    #processed_path = preprocess_image(image_path)
    processed_path = image_path

    # Configurazione avanzata di Tesseract
    custom_config = r'--oem 3 --psm 6'  # Mode di riconoscimento ottimale per testo standard
    text = pytesseract.image_to_string(Image.open(processed_path), config=custom_config)
    
    #os.remove(processed_path)  # Elimina il file temporaneo
    return text.strip()

def index_images():
    """ Indicizza le immagini e salva i dati nel database """
    for filename in os.listdir(IMG_FOLDER):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(IMG_FOLDER, filename)
            text = extract_text_from_image(img_path)

            cursor.execute("INSERT OR REPLACE INTO images (filename, text) VALUES (?, ?)", (filename, text))
            conn.commit()
            print(f"✅ Indicizzata: {filename}")

index_images()
conn.close()
