You cannot open the showGraph.html directly. You will see error: 
			XMLHttpRequest cannot load file: blabla...

Reason: You need a local server to load json, because d3.json is meant to load data through HTTP. 

Solution: Install Brackets, and then launch webpage from it.