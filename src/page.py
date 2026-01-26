# page.py
from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string(open("upload.html").read())

@app.route("/health")
def health():
    return "ok", 200

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file or not file.filename.endswith(".pdf"):
        return jsonify({"message": "Invalid file"}), 400
    return jsonify({"message": "PDF uploaded and processed successfully"})

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)
