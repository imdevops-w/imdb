import requests
from bs4 import BeautifulSoup
import json
import html
import os


def get_movie_data(imdb_id):
    import requests
    from bs4 import BeautifulSoup
    import json

    url = f"https://www.imdb.com/title/{imdb_id}/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": "Movie not found or IMDb blocked request"}

    soup = BeautifulSoup(response.text, "html.parser")

    ld_json = soup.find("script", type="application/ld+json")
    if not ld_json:
        return {"error": "Metadata not found"}
    
    data = json.loads(ld_json.string)

    def extract_text(label):
        try:
            for li in soup.select("li.ipc-metadata-list__item"):
                if li.find("span") and label.lower() in li.find("span").text.lower():
                    return ", ".join([a.text.strip() for a in li.find_all("a")])

            all_text = soup.get_text()
            if label.lower() in all_text.lower():
                return label + " found in raw text"
        except:
            pass
        return "N/A"


    country = extract_text("Country of origin")
    language = extract_text("Language")

    movie_data = {
        "imdbID": imdb_id,
        "title": html.unescape(data.get("name", "N/A")),
        "year": data.get("datePublished", "N/A")[:4],
        "imdbRating": data.get("aggregateRating", {}).get("ratingValue", "N/A"),
        "runtime": data.get("duration", "N/A").replace("PT", "").lower(),
        "genre": ", ".join(data.get("genre", [])) if isinstance(data.get("genre"), list) else data.get("genre", "N/A"),
        "country": country,
        "language": language,
        "director": ", ".join([d.get("name") for d in data.get("director", [])]) if isinstance(data.get("director"), list) else data.get("director", {}).get("name", "N/A"),
        "writer": ", ".join([w.get("name") for w in data.get("creator", []) if w.get("@type") == "Person"]) if "creator" in data else "N/A",
        "actors": ", ".join([a.get("name") for a in data.get("actor", [])]) if "actor" in data else "N/A",
        "poster": data.get("image", "")
    }

    save_dir = "saved_data"
    os.makedirs(save_dir, exist_ok=True)  
    
    save_path = os.path.join(save_dir, f"{imdb_id}.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(movie_data, f, ensure_ascii=False, indent=4)
        
    return movie_data
