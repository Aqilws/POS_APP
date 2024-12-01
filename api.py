from flask import Flask, jsonify

app = Flask(__name__)

menu = [
    {"id": 1, "nama": "Nasi Goreng", "deskripsi": "Nasi goreng khas Indonesia", "harga": 15000, "foto": "nasi_goreng.jpg"},
    {"id": 2, "nama": "Sate Ayam", "deskripsi": "Sate ayam dengan bumbu kacang", "harga": 25000, "foto": "sate_ayam.jpeg"},
    {"id": 3, "nama": "Es Teh", "deskripsi": "Teh manis dengan es batu", "harga": 5000, "foto": "es_tesh.jpg"},
]

@app.route('/menu', methods=['GET'])
def get_menu():
    return jsonify(menu)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
