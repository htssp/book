from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

def search_books(query, max_results=9):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}"
    response = requests.get(url)
    data = response.json()

    books = []
    if "items" in data:
        for item in data["items"]:
            volume_info = item.get("volumeInfo", {})
            book = {
                "title": volume_info.get("title", "No title"),
                "authors": ", ".join(volume_info.get("authors", ["Unknown"])),
                "description": volume_info.get("description", "No description"),
                "thumbnail": volume_info.get("imageLinks", {}).get("thumbnail", ""),
                "link": volume_info.get("infoLink", "")
            }
            books.append(book)
    return books

def get_popular_books():
    # Rotate through different queries for variety
    queries = [
        "bestsellers",
        "popular fiction",
        "classic literature",
        "young adult novels",
        "fantasy ",
        "science fiction",
        "romance novels",
        "thrillers",
        "mystery novels",
        "self help"
    ]
    query = random.choice(queries)
    return search_books(query, max_results=12), query

@app.route("/", methods=["GET", "POST"])
def index():
    books = []
    query = ""

    # Manual search
    if request.method == "POST":
        query = request.form["query"]
        books = search_books(query)

    # Genre selection
    genre = request.args.get("genre")
    if genre:
        query = genre
        books = search_books(genre)

    # Popular books only if no search/genre
    popular, popular_query = ([], "")
    if not books and not query:
        popular, popular_query = get_popular_books()

    return render_template("index.html", books=books, query=query,
                           popular=popular, popular_query=popular_query)

if __name__ == "__main__":
    app.run(debug=True)
