Story Analysis UI Demo
=======

### Introduction
This demo page is for entity relationship extraction. The user may input some texts in the textarea and get 
the entities and relationships in the texts by simply clicking the submit button. If any relationships found 
in the text, three tables will show up and display the extracted relationships, ranking of the extractions, 
and ranking of the entities respectively. To make the result vivid, a graph is developed to display the 
entities as nodes and relationships as links.     

The demo page for entity relationship extraction is developed with Flask as the backend and its Jinjia2 template 
as the frontend. The result tables are simply converted from dataframes of pandas library with to_html method. 
The graph is implemented with D3.v3.js.

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
* JQuery, 
Bootstrap, 
D3.v3.js  
```
	//Add them to the html page directly.
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<script src="https://d3js.org/d3.v3.min.js"></script>
```

Here are some resources for [Flask](http://flask.pocoo.org/docs/0.12/) and 
[D3.js](https://www.youtube.com/watch?v=n5NcCoa9dDU&list=PL6il2r9i3BqH9PmbOf5wA5E1wOG3FT22p). 
You may find more examples and tutorials online. 

### Usage
```
	python run.py
```
See http://localhost:5000


### Appearance
