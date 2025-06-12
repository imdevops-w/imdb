import os
import requests
from flask import Flask, request, jsonify
from imdb import IMDb

app = Flask(__name__)

# Setup sources
ia = IMDb()  # faster scraping
OMDB_API_KEY = os.getenv("e63afbdc")
TMDB_API_KEY = os.getenv("b5b80f499caa4c0c95b4205ae470fb14")

@app.route('/', methods=['GET'])
def get_movie():
    imdb_id = request.args.get('imdbID')
    if not imdb_id:
        return jsonify({"error": "imdbID parameter is required"}), 400

    # 1) Try OMDb first
    omdb = None
    if OMDB_API_KEY:
        r = requests.get(
            "https://www.omdbapi.com/",
            params={"apikey": OMDB_API_KEY, "i": imdb_id}
        )
        if r.status_code == 200:
            omdb = r.json()
            if omdb.get("Response") != "True":
                omdb = None

    # 2) Try TMDb fallback
    tmdb_data = None
    if TMDB_API_KEY and not omdb:
        t = requests.get(
            f"https://api.themoviedb.org/3/find/{imdb_id}",
            params={"api_key": TMDB_API_KEY, "external_source": "imdb_id"}
        )
        if t.status_code == 200:
            arr = t.json().get("movie_results") or []
            if arr:
                tmdb_data = arr[0]

    # 3) If still no data, fallback to IMDbPY
    ia_data = None
    if not omdb and not tmdb_data:
        try:
            raw = ia.get_movie(imdb_id.replace("tt", ""))
            ia_data = raw
        except Exception as e:
            return jsonify({
                "error": "All sources failed",
                "omdb": omdb, "tmdb": tmdb_data, "impy": str(e)
            }), 500

    # Merge data
    def pick(field, *sources):
        for src in sources:
            if src and src.get(field):
                return src.get(field)
        return "N/A"

    def safe_list(items):
        return ", ".join([i.get("name") for i in items]) or "N/A"

    data = {
        "imdbID": imdb_id,
        "title": pick("Title", omdb, ia_data and ia_data.data, tmdb_data),
        "year": pick("Year", omdb, ia_data and ia_data.data, tmdb_data),
        "runtime": pick("Runtime", omdb, ia_data and ia_data.data, tmdb_data),
        "imdbRating": pick("imdbRating", omdb, ia_data and ia_data.data),
        "rottenTomatoes": next((i["Value"] for i in (omdb.get("Ratings") or [])
                                if i["Source"] == "Rotten Tomatoes"), "N/A") if omdb else "N/A",
        "country": pick("Country", omdb),
        "language": pick("Language", omdb),
        "genre": pick("Genre", omdb),
        "director": pick("Director", omdb),
        "writer": pick("Writer", omdb),
        "actors": pick("Actors", omdb),
        "poster": pick("Poster", omdb, ia_data and ia_data.data, tmdb_data and {"cover_url": tmdb_data.get("poster_path")}),
    }
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
