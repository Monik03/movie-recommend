from flask import Flask, render_template, request
import requests
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NmYwYWQ0MTAwNzFkOGI2ZTAyNjU3MjhiOGEyMGQ1NyIsInN1YiI6IjY1ZTVkNGQwYTA1NWVmMDE3YzEyMTA4YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.YOp72kVV7A8JSemgSffEVZqX5kc3Ws8EJxiXYIZrToI"
    }

def processNouns(s):
    s=s.lower()
    print(s, "\n")
    words=nltk.word_tokenize(s)
    words=set(words)
    print(words, "\n")
    sw = stopwords.words("english")
    without_sw=[]
    for i in words:
        if i not in sw:
            without_sw.append(i)
    onlyAlpha = []
    for i in without_sw:
        if(i.isalpha()):
            onlyAlpha.append(i)
    print("\n", onlyAlpha)            
    lemma = WordNetLemmatizer()
    lemma_out = [lemma.lemmatize(i) for i in onlyAlpha]
    # print(lemma_out)
    # stemmer = SnowballStemmer('english')
    # stemList = [stemmer.stem(i) for i in lemma_out]
    # print(stemList)
    tupleListTags = nltk.pos_tag(lemma_out)
    print("\n", tupleListTags)
    nounsList=[]
    for tup in tupleListTags:
        if(tup[1]=="NN" or tup[1]=="NNS" or tup[1]=='NNP' or tup[1]=='NNPS' or tup[1]=='JJ' or tup[1]=='JJR' or tup[1]=='JJS'):
            nounsList.append(tup[0])
    print("\n", nounsList)
    return nounsList

app = Flask(__name__)
# o={1:"animal",2:"bird",3:"human",4:"alien"}

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/dic/")
def discover():
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        return render_template("index.html", err='You are not connected to the internet!')
    except requests.exceptions.ReadTimeout:
        return render_template("index.html", err='Fetching movies took too long.')
    except:
        return render_template("index.html", err='Failed to load movies')
    else:
        return render_template("index.html", trending=response.json()["results"])  #extracting json response from object and a 'results' list from this dictionary.

@app.route("/recommend", methods=['post'])
def recommend():
    sentence = request.form.get("sentence")
    nouns = processNouns(sentence)
    keyIdMap=[]
    if(len(nouns)==0):
        return render_template("index.html", err="No nouns found in your input!")
    for kword in nouns:
        keyIdUrl = "https://api.themoviedb.org/3/search/keyword?query="+kword+"&page=1"
        try:
            res = requests.get(keyIdUrl, headers=headers, timeout=5)
        except:
            print("\nCan't fetch keyword Id")
            continue
        keyIdMap.append(res.json()["results"][0])
    if(len(keyIdMap)==0):
        return render_template("index.html", err="Can't fetch keyIds right now.")
    print(keyIdMap)
    kwMovieURL="https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_keywords="
    for kw_dic in keyIdMap:
        kwMovieURL+=str(kw_dic["id"])+"|"
    kwMovieURL=kwMovieURL.rstrip("|")
    print("\n", kwMovieURL)
    try:
        res = requests.get(kwMovieURL, headers=headers, timeout=5)
    except:
        return render_template("index.html", err="Can't fetch movies from keyIDs")
    return render_template("index.html", input=sentence, out=res.json()["results"])

if __name__=='__main__':
    app.run()