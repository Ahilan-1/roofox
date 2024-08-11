from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "AIzaSyAILThGOI1oeP1Jw_sj7gBsMYywgt7VnBs"
CSE_ID = "b335bda5780904391"

def google_search(query, search_type='web'):
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CSE_ID}&q={query}"
    if search_type == 'image':
        url += "&searchType=image"
    elif search_type == 'news':
        url += "&num=10"  # Fetch up to 10 news results

    response = requests.get(url)
    return response.json()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    search_type = request.form.get('search_type', 'web')
    
    search_results = google_search(query, search_type)
    results = []
    
    if 'items' in search_results:
        for item in search_results['items']:
            result = {
                'title': item['title'],
                'link': item['link'],
                'snippet': item.get('snippet', '')
            }
            if search_type == 'image':
                # Use the direct image link provided by the API
                result['image'] = item.get('link', '')
            elif search_type == 'news':
                result['source'] = item.get('displayLink', '')
            results.append(result)
    
    return render_template('results.html', query=query, results=results, search_type=search_type)

if __name__ == '__main__':
    app.run(debug=True)