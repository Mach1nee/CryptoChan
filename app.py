import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Pasta para armazenar uploads
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Função para inicializar o banco de dados
def init_db():
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    # Removido o comando DROP TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY, 
                    username TEXT, 
                    content TEXT, 
                    image_url TEXT, 
                    timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('Crypto.html')

@app.route('/1337')
def hack():
    return render_template('1337.html')

@app.route('/Detrew')
def Detrew():
    return render_template('Detrew.html')

@app.route('/post', methods=['POST'])
def post():
    data = request.form
    username = data['username'] or 'Anonymous'
    content = data['content']
    
    image_url = None
    if 'image' in request.files and request.files['image'].filename != '':
        image_file = request.files['image']
        image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(image_filename)
        image_url = f"/uploads/{image_file.filename}"

    # Obtém a hora atual em UTC e ajusta para o horário de Brasília (UTC-3)
    timestamp = (datetime.now(timezone.utc) - timedelta(hours=3)).isoformat()
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts (username, content, image_url, timestamp) VALUES (?, ?, ?, ?)", 
               (username, content, image_url, timestamp))
    conn.commit()
    post_id = c.lastrowid
    conn.close()
    
    return jsonify({'id': post_id, 'username': username, 'content': content, 'imageUrl': image_url, 'timestamp': timestamp})

@app.route('/posts', methods=['GET'])
def get_posts():
    conn = sqlite3.connect('forum.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    
    return jsonify([{'id': post[0], 'username': post[1], 'content': post[2], 'imageUrl': post[3], 'timestamp': post[4]} for post in posts])

@app.route('/uploads/<path:filename>', methods=['GET'])
def send_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados apenas uma vez
    app.run(debug=True, port=5000)