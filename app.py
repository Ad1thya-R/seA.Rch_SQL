from flask import Flask, request, jsonify
from search import search
from filter import Filter
from storage import DBStorage
import html

styles = """
<style>
    .result2 {
        width: auto;
        height: auto;
        overflow:auto;
        rgba(69, 69, 69, 0.3);
    }
    .result1 {
        width: auto;
        height: auto;
        overflow:auto;
        background-color: rgba(138, 0, 0, 0.3);
    }
    .site {
        font-size: .8rem;
        color: green;
    }

    .snippet {
        font-size: .9rem;
        color: gray;
        margin-bottom: 30px;
    }

    .rel-button {
        cursor: pointer;
        color: blue;
    }
    
    .centerImage {
        display: flex;
        align-items: center;
        justify-content: center;

    }
    .searchbar {
        margin-top: 100px
        width: 100%;
        max-width: 800px;
        display: inline-flex;
    }
    
    .searchbar__input {
        flex-grow: 1;
        padding: 10px;
        outline: none;
        border: 1px solid #e90000;
        border-radius: 5px 0 0 5px;
        background: rgba(188, 0, 0, 0.2);
        transition: background 0.25s, box-shadow 0.25s;
    }
    
    .searchbar__input:focus {
        background: white;
        box-shadow: 0 0 2px #640000;
    }
    
    .searchbar__input::placeholder {
        color: #e90000;
    }
    
    .searchbar__button {
        width: 40px;
        background: #e90000;
        color: #ffffff;
        outline: none;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 0 5px 5px 0;
        cursor: pointer;
        user-select: none;
    }
    
    .searchbar__button:active {
        box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.25);
    }
    
</style>
<script>
const relevant = function(query, link){
    fetch("/relevant", {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
           "query": query,
           "link": link
          })
        });
}
</script>
"""


search_template = styles + """
    <div class="centerImage">
    <img src="static/logo.png" class="centerImage" />
    </div>
    <div class="centerImage">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
     <form action="/" method="post">
         <div class="searchbar">
            <input type="text" name="query" class="searchbar__input" placeholder="Search">
            <button type="submit" class="searchbar__button">
            <i class="material-icons">search</i>
            </button>
        </div>
    </form> 
    </div>
    """

result_template1 = """
<div class="result1">
    <p class="site">{rank}: {link} <span class="rel-button" onclick='relevant("{query}", "{link}");'>Relevant</span></p>
    <a href="{link}">{title}</a>
    <p class="snippet">{snippet}</p>
</div>
"""

result_template2 = """
<div class="result2">
    <p class="site">{rank}: {link} <span class="rel-button" onclick='relevant("{query}", "{link}");'>Relevant</span></p>
    <a href="{link}">{title}</a>
    <p class="snippet">{snippet}</p>
</div>
"""

def show_search_form():
    return search_template

def run_search(query):
    results = search(query)
    fi = Filter(results)
    results = fi.filter()
    rendered = search_template
    results["snippet"] = results["snippet"].apply(lambda x: html.escape(x))

    counter=0
    for index, row in results.iterrows():
        if counter%2==0:
            rendered += result_template1.format(**row)
        else:
            rendered += result_template2.format(**row)
        counter+=1
    return rendered


app = Flask(__name__, static_url_path='/static')
@app.route("/", methods=['GET', 'POST'])

def search_form():
    '''

    :return:
    '''
    if request.method == 'POST':
        query = request.form["query"]
        return run_search(query)
    else:
        return show_search_form()

@app.route("/relevant", methods=["POST"])
def mark_relevant():
    data = request.get_json()
    query = data["query"]
    link = data["link"]
    storage = DBStorage()
    storage.update_relevance(query, link, 10)
    return jsonify(success=True)