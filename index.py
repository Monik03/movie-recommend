from flask import Flask, render_template, request
import requests
import nltk
from nltk.corpus import stopwords

def processNouns(s):
    s=s.lower().isalpha()
    words=nltk.word_tokenize(s)
    sw = stopwords.words("english")

app = Flask(__name__)
# o={1:"animal",2:"bird",3:"human",4:"alien"}

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/dic/")
def discover():
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NmYwYWQ0MTAwNzFkOGI2ZTAyNjU3MjhiOGEyMGQ1NyIsInN1YiI6IjY1ZTVkNGQwYTA1NWVmMDE3YzEyMTA4YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.YOp72kVV7A8JSemgSffEVZqX5kc3Ws8EJxiXYIZrToI"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        return render_template("index.html", err='You are not connected to the internet!')
    except requests.exceptions.ReadTimeout:
        return render_template("index.html", err='Fetching movies took too long.')
    except:
        return render_template("index.html", err='Failed to load movies')
    else:
        return render_template("index.html", out=response.json()["results"])  #extracting json response from object and a 'results' list from this dictionary.

@app.route("/recommend", methods=['post'])
def recommend():
    sentence = request.form.get("sentence")
    nouns = processNouns(sentence)
    return render_template("index.html", input=sentence)

if __name__=='__main__':
    app.run()