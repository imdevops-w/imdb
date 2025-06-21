from flask import Flask, request, jsonify
import os
import json
from scraper import get_movie_data

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    imdb_id = request.args.get("imdbID")
    if not imdb_id:
        return jsonify({"error": "Missing imdbID"}), 400

    filepath = f"data/{imdb_id}.json"

    try:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = get_movie_data(imdb_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
