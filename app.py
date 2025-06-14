from flask import Flask, request, jsonify
from scraper import get_movie_data

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    imdb_id = request.args.get("imdbID")
    if not imdb_id:
        return jsonify({"error": "Missing imdbID"}), 400
    try:
        data = get_movie_data(imdb_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
