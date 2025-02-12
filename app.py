from flask import Flask, jsonify, render_template, send_from_directory
import sqlite3
import os

# creates a Flask application
app = Flask(__name__)

# Database file (adjust path if needed)
DATABASE = 'images.db'

# Path to your screenshot folder (relative to your Flask app)
SCREENSHOT_FOLDER = 'screenshots'  # Or a full absolute path

# Make the screenshot folder accessible via /screenshots URL prefix
app.add_url_rule('/screenshots/<path:path>', endpoint='screenshots', view_func=lambda path: send_from_directory(SCREENSHOT_FOLDER, path))

# Ensure the folder exists (good practice)
if not os.path.exists(SCREENSHOT_FOLDER):
    os.makedirs(SCREENSHOT_FOLDER)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Return dictionaries for rows
    return conn

@app.route('/images', methods=['GET'])
def get_images():
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        filename_search = request.args.get('filename')
        text_search = request.args.get('text')

        sql_query = "SELECT id, filename, text FROM images"
        query_params = []

        if filename_search:
            sql_query += " WHERE filename LIKE ?"
            query_params.append(f"%{filename_search}%")

        if text_search:
            if filename_search:  # Check if filename search already added a WHERE clause
                sql_query += " AND text LIKE ?"
            else:
                sql_query += " WHERE text LIKE ?"
            query_params.append(f"%{text_search}%")

        cur.execute(sql_query, query_params)
        rows = cur.fetchall()
        images = []

        for row in rows:
            images.append({
                'id': row['id'],
                'filename': row['filename'],
                'text': row['text']
            })

        conn.close()
        return jsonify(images)

    except sqlite3.Error as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route("/")
def home():
    return render_template('home.html')

# run the application 
if __name__ == "__main__": 
    from flask import request  # Import request here
    app.run(debug=True)