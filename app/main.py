import os, time
from flask import Flask, render_template, request, redirect, url_for
from minio import Minio
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Ambil dari env atau pakai default
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "taskdb")
MINIO_USER = os.getenv("MINIO_USER", "user")
MINIO_PASS = os.getenv("MINIO_PASSWORD", "password")

BUCKET_NAME = "taskbucket"
MINIO_CLIENT = Minio("minio:9000", access_key=MINIO_USER, secret_key=MINIO_PASS, secure=False)

def get_db_connection():
    return psycopg2.connect(host="db", database=DB_NAME, user=DB_USER, password=DB_PASS)

def init_db():
    print("Sedang menyiapkan database... ⏳")
    for i in range(10):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS submissions (
                    id SERIAL PRIMARY KEY,
                    assignment_name VARCHAR(100),
                    file_path TEXT,
                    submit_time TIMESTAMP,
                    status VARCHAR(20)
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Database Siap! ✅")
            return
        except:
            time.sleep(2)

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT assignment_name, file_path, submit_time, status FROM submissions ORDER BY submit_time DESC")
            data = cur.fetchall()
        except psycopg2.errors.UndefinedTable:
            conn.rollback()
            init_db()
            data = []
        cur.close()
        conn.close()
        return render_template('index.html', submissions=data)
    except Exception as e:
        return f"Waduh Mimii, ada masalah koneksi: {str(e)}"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file_tugas')
    name = request.form.get('assignment_name')
    if file and name:
        if not MINIO_CLIENT.bucket_exists(BUCKET_NAME):
            MINIO_CLIENT.make_bucket(BUCKET_NAME)
        MINIO_CLIENT.put_object(BUCKET_NAME, file.filename, file, length=-1, part_size=10*1024*1024)
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO submissions (assignment_name, file_path, submit_time, status) VALUES (%s, %s, %s, %s)",
                    (name, file.filename, datetime.now(), "Berhasil"))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
