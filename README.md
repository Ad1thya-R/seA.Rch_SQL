# seA.Rch_SQL

Uses Google programmable search engine API to scrape web for results. Filtered and ranked results with SQL queries based on sentence length and
vocabulary used. Built web application on Flask to display search engine’s functionality.



https://user-images.githubusercontent.com/46827614/192603207-6d64afb3-c92a-4443-9d2c-1e539b9ebf04.mov



File overview:

* `app.py` - the web interface
* `filter.py` - the code to filter results
* `search.py` - code to get the search results
* `settings.py` - settings needed by the other files
* `storage.py` - code to save the results to a database

# Local Setup

## Installation

To follow this project, please install the following locally:

* Python 3.9+
* Required Python packages (`pip install -r requirements.txt`)

### Other setup

You will need to create a programmable search engine and get an API key by following [these directions](https://developers.google.com/custom-search/v1/introduction).  
You will need a Google account, and as part of this you may also need to sign up for Google Cloud.

## Run

Run the project with:

* `pip install -r requirements.txt`
* `flask --debug run --port 5001`

