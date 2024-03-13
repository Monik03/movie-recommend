import requests

url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2NmYwYWQ0MTAwNzFkOGI2ZTAyNjU3MjhiOGEyMGQ1NyIsInN1YiI6IjY1ZTVkNGQwYTA1NWVmMDE3YzEyMTA4YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.YOp72kVV7A8JSemgSffEVZqX5kc3Ws8EJxiXYIZrToI"
}

response = requests.get(url, headers=headers)

print(resList)