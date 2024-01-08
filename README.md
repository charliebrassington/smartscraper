# Smartscraper
Smartscraper is a simple microservice which automatically classifies and parses web pages using AI

## Run With Docker
```commandline
docker build -t smartscraper-application .
docker run -p 5000:5000 --name smartscraper-application-1 smartscraper-application
```

## Usage

### Train Both Models
```python
import requests

requests.post("http://127.0.0.1:5000/api/model/train", json={"name": "json"}).json() # {'success': 'the model has been trained'}
requests.post("http://127.0.0.1:5000/api/model/train", json={"name": "html"}).json() # {'success': 'the model has been trained'}
```

### Scrape Sites
This will not work if the html AND json models have not been trained (follow the example above)
```python
import requests

response = requests.post("http://127.0.0.1:5000/api/scrape", json={"url": "https://medal.tv/u/sonographysono"})
response.json()
"""
 {
    'success': 'successfully scraped the url'
    'result': {
        'follower_count': ['profiles-3049482-followers: 3'], 
        'following_count': ['profiles-3049482-following: 1'], 
        'json': ['<script>var Vr0draJ......']
    }
}
"""

```

### Editing Datasets
- Both datasets can be found in the "datasets" folder
- The HTML dataset has a key for label and html, html contains the element label contains the classification for the html
- The JSON dataset is similar it has a key for label and json, json contains the flattened key and value, label contains the classification
- If the model is collecting something you don't want, in the html dataset give it the label "unwanted" if its the json dataset give it the label "unknown"


## Roadmap
- Add validation for both the url and name
- Catch errors if the model fails to guess the correct json label and fails to parse the raw json
- Catch errors when both models are not trained and sites are being scraped
- Modification of the training iterators (new param)
- Unit and integration tests for the important parts
- Try and figure out a way to replicate an API req dynamically based on the site javascript
- More html and json datasets
