import os
import joblib
from index import Index
from functools import lru_cache
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
pre_index = Index()

target = "data/index_dump-small.joblib"
print("Loading Index")
size_in_bytes = os.path.getsize(target)
size_in_mb = size_in_bytes / (1024 * 1024)
print("Size in megabytes", size_in_mb)

# Define a cache object
cache = {}

# Define a function to generate cache keys
def get_cache_key(query):
    return query.lower()

# Define a function to store values in the cache
def set_cache(key, value):
    cache[key] = value

# Define a function to retrieve values from the cache
def get_cache(key):
    return cache.get(key)

# Define a decorator to add caching to the search function
def cache_search(func):
    @lru_cache(maxsize=128)
    def wrapper(query, rank=True):
        cache_key = get_cache_key(query)
        cached_result = get_cache(cache_key)
        if cached_result is not None:
            return cached_result
        result = func(query, rank)
        set_cache(cache_key, result)
        return result
    return wrapper

# Apply the cache_search decorator to the search method of the pre_index object
pre_index.search = cache_search(pre_index.search)

pre_index = joblib.load(target)    #load the .joblib file

print("Index Loaded")

@app.route('/search', methods=['POST'])
@cross_origin()
def search():
    query = request.form.get('query')
    print("query :", query)

    # Get the selected search type from the radio buttons
    search_type = request.form.get('search_type')

    # Call the search method of the pre_index object with the selected search type
    res = pre_index.search(query, search_type, rank=True)

    results = []
    for doc in res[:5]:
        title = doc[0].title
        url = doc[0].url
        results.append({'title': title, 'url': url})

    print(jsonify({'results': results}).json)
    return jsonify({'results': results}).json

if __name__ == '__main__':
    app.run(port=5000)
