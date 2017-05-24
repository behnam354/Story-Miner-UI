Story Analysis UI Demo
=======

This demo page is for entity relationship extraction. The user may input some texts in the textarea and get 
the entities and relationships in the texts by simply clicking the submit button. If any relationships found 
in the text, three tables will show up and display the extracted relationships, ranking of the extractions, 
and ranking of the entities respectively. To make the result vivid, a graph is developed to display the 
entities as nodes and relationships as links.     

The demo page for entity relationship extraction is developed with [Flask](http://flask.pocoo.org/docs/0.12/).  
The graph is implemented with [D3.v3.js](https://d3js.org/).

### Dependencies
* practnlptools 
download from https://github.com/biplab-iitb/practNLPTools
```
	python setup.py install
```
* nxpd: 	
```
	sudo pip install nxpd
```
* nltk: 	
```
	sudo pip install nltk
	python -m nltk.downloader all
```
* Flask 0.10.1 
```
	sudo pip install Flask
	sudo pip install flask_wtf
```



### Usage
```
	python run.py
```
See the webpage at http://localhost:5000


### Appearance
