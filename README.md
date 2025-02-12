# py-ocr-image-search
Flask App che scansiona con OCR una libreria di immagini e successivamente permette di cercare stringhe di testo contenute in tali immagini.

<br>

## Come utilizzare il tool
### 1. Setup iniziale
- Creare una cartella `screenshots` nella cartella root del progetto ed inserire al suo interno le immagini da elaborare.
- Creare un `virtual enviorment` python con il comando:
```shell
python -m venv venv
```
- Attivare l'ambiente virtuale con il comando:
```shell
source venv/bin/activate
```
- Installare i pacchetti python necessari con il comando:
```shell
pip install -r requirements.txt
```
### 2. Scansione OCR e creazione del database
- Eseguire lo script python `extract_text.py` con il comando:
```shell
python extract_text.py
```
><br>Lo script elaborerà tutte le immagini nella cartella `screenshot` e genererà un database `images.db` contenente una tabella con il testo etrapolato dalle singole immagini<br><br>
### 3. Avviare l'app
- Eseguire lo script python `app.py` con il comando:
```shell
python app.py
```
- Visitare la pagina `http://127.0.0.1:5000/` per utilizzare la GUI.
- Inserire nel campo di input la stringa di testo da ricercare.
- L'app presenterà il risultato della ricerca in un layout a card, con la possibilitò di aprire a schermo intero ogni singola immagine risultante.

<br>

## Info
Per migliorare il riconoscimento OCR con `pytesseract`, si possiamo applicare pre-processing alle immagini prima dell'analisi.
Alcune ottimizzazioni includono:

✅ **Conversione in scala di grigi** per ridurre il rumore<br>
✅ **Binarizzazione (thresholding)** per migliorare il contrasto<br>
✅ **Ridimensionamento** per una maggiore accuratezza<br>
✅ **Rimozione del rumore** con filtri OpenCV<br>
✅ **Uso di modalità OCR ottimizzate** con `--psm` e `--oem`<br>

<br>

🔍 Miglioramenti rispetto alla versione *base*
1. **Pre-processing avanzato con OpenCV**
    - **Riduzione rumore** (`cv2.bilateralFilter`)
    - **Binarizzazione migliorata** (`cv2.THRESH_OTSU`)
    - **Scala di grigi** per ridurre il peso computazionale
    - **Ridimensionamento** (`cv2.resize`) per un OCR più accurato
2. **Migliore configurazione di Tesseract**
    - `--oem 3`: Modalità avanzata per migliorare l'accuratezza
    - `--psm 6`: Ideale per blocchi di testo standard
3. **Più efficiente e automatico**
    - **Eliminazione automatica** delle immagini temporanee
    - **Ottimizzazione del database** con `INSERT OR REPLACE`