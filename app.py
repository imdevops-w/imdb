import os
from flask import Flask, request, jsonify
from imdb import IMDb

app = Flask(__name__)
ia = IMDb()

@app.route('/', methods=['GET'])
def get_movie():
    imdb_id = request.args.get('imdbID')
    if not imdb_id:
        return jsonify({"error": "imdbID parameter is required"}), 400

    try:
        movie = ia.get_movie(imdb_id.replace("tt", ""))

        def safe_list(items):
            return ", ".join([p.get("name", "N/A") for p in items]) if items else "N/A"

        data = {
            "imdbID": imdb_id,
            "title": movie.get("title", "N/A"),
            "year": str(movie.get("year", "N/A")),
            "rottenTomatoes": "N/A",
            "imdbRating": str(movie.get("rating", "N/A")),
            "runtime": movie.get("runtimes", ["N/A"])[0] + " min" if movie.get("runtimes") else "N/A",
            "country": ", ".join(movie.get("countries", [])) or "N/A",
            "language": ", ".join(movie.get("languages", [])) or "N/A",
            "genre": ", ".join(movie.get("genres", [])) or "N/A",
            "director": safe_list(movie.get("directors", [])),
            "writer": safe_list(movie.get("writers", [])),
            "actors": safe_list(movie.get("cast", [])[:5]),
            "poster": movie.get("cover url", "")
        }
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": "Failed to fetch movie details", "details": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
