	function drawGraph(dataset){
			// parameters
			var w = 500;//canvas
			var h = 600;//canvas
			var dx = 30;//edgeLabel relative position
			var dy = -10;//edgeLabel relative position
			var r = 15;//radius
			var fontSize = 15;
			var defaultColor = '#ccc'
			//var linkDistance=200;
			var colors = d3.scale.category10();
			
			// zoom
			var zoom = d3.behavior.zoom()
				.on("zoom", function () {
					svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
				});
			
			// drag
			var drag = d3.behavior.drag()
				.origin(function(d) { return d; })
				.on("dragstart", dragstarted)
				.on("drag", dragged)
				.on("dragend", dragended);
			
			
			function dragstarted(d) {
			  d3.event.sourceEvent.stopPropagation();			  
			  d3.select(this).classed("dragging", true);
			  // deregister listeners
              d3.select(this).on("mouseover", null).on("mouseout", null); 
			  force.start();
			}

			function dragged(d) {			  
			  d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);
			}

			function dragended(d) {			  
			  d3.select(this).classed("dragging", false);
			  //reregisters listeners
              d3.select(this).on("mouseover", mouseover).on("mouseout", mouseout); 
			}

			// svg
			var svg = d3.select("div#chartId")
			   .append("div")
			   //.style('background-color',defaultColor)
			   .classed("svg-container", true) //container class to make it responsive
			   .append("svg")
			   //.attr({"width":w,"height":h})
			   //responsive SVG needs these 2 attributes and no width and height attr
			   .attr("preserveAspectRatio", "xMinYMin meet")
			   .attr("viewBox", "0 0 600 400")
			   //class to make it responsive
			   .classed("svg-content-responsive", true)
				  .attr("width", "100%")
				  .attr("height", "100%")
				  .call(zoom)
				  .append("g");


			// force layout
			var force = d3.layout.force()
				.nodes(dataset.nodes)
				.links(dataset.links)
				.size([w,h])
				//.linkDistance([linkDistance])
				.linkDistance(function(d){return d.label.length * 10 + dx * 2;})
				.charge([-500])
				.theta(0.1)
				.gravity(0.05)
				.start();

			// edges
			var links = svg.selectAll("line")
			  .data(dataset.links)
			  .enter()
			  .append("line")
			  .attr("id",function(d,i) {return 'edge'+i})
			  .attr('marker-end','url(#arrowhead)')
			  .style("stroke",defaultColor)
			  .style("pointer-events", "none");
			
			// vertexes
			var nodes = svg.selectAll("circle")
			  .data(dataset.nodes)
			  .enter()
			  .append("circle")
			  .attr({"r":r})
			  .style("fill",function(d,i){return colors(i);})
			  .call(drag)

			// node labels
			var nodelabels = svg.selectAll(".nodelabel") 
			   .data(dataset.nodes)
			   .enter()
			   .append("text")
			   .attr({'font-size':fontSize,
					  "x":function(d){return d.x;},
					  "y":function(d){return d.y;},
					  "class":"nodelabel",
					  "stroke":"black",
					  'transform': 'translate(10, -10)'
					  })
			   .text(function(d){return d.id;});
			   
			// edge paths and labels
			var edgepaths = svg.selectAll(".edgepath")
				.data(dataset.links)
				.enter()
				.append('path')
				.attr({"id": function(d,i) {return 'edgepath'+i},
					   'd': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
					   'class':'edgepath',
					   'fill-opacity':0,
					   'stroke-opacity':0,
					   'fill':'blue',
					   'stroke':'red',
					 })
				.style("pointer-events", "none");

			var edgelabels = svg.selectAll(".edgelabel")
				.data(dataset.links)
				.enter()
				.append('text')
				.style("pointer-events", "none")
				.attr({'class':'edgelabel',
					   'id':function(d,i){return 'edgelabel'+i},
					   'dx':dx,
					   'dy':dy,
					   'font-size':fontSize,
					   'fill':defaultColor});

			edgelabels.append('textPath')
				.attr('xlink:href',function(d,i) {return '#edgepath'+i})
				.style("pointer-events", "none")
				.text(function(d,i){return d.label});

			// #ccc arrow head 
			svg.append('defs').append('marker')
				.attr({'id':'arrowhead',
					   'viewBox':'-0 -5 10 10',
					   'refX':25,
					   'refY':0,
					   //'markerUnits':'strokeWidth',
					   'orient':'auto',
					   'markerWidth':10,
					   'markerHeight':10,
					   'xoverflow':'visible'})
				.append('svg:path')
					.attr('d', 'M 0,-5 L 10 ,0 L 0,5')
					.attr('fill', defaultColor)
					.attr('stroke', defaultColor);
			
			// black arrow head 
			svg.append('defs').append('marker')
				.attr({'id':'arrowhead1',
					   'viewBox':'-0 -5 10 10',
					   'refX':25,
					   'refY':0,
					   //'markerUnits':'strokeWidth',
					   'orient':'auto',
					   'markerWidth':10,
					   'markerHeight':10,
					   'xoverflow':'visible'})
				.append('svg:path')
					.attr('d', 'M 0,-5 L 10 ,0 L 0,5')
					.attr('fill', 'black')
					.attr('stroke','black');
			
			
			// highlight neighbors
			
			var neighborList = {}	// hash map to store neighbors fetched	
			var duration = 500;
			function highlightNeighbors(d) {
				// get neighbors from hash map
				if (d.id in neighborList) { // contains key
					nodeNeighbors = neighborList[d.id];
					console.log("hashmap");
				}
				else {
					nodeNeighbors = findNeighbors(d);
					neighborList[d.id] = nodeNeighbors;
					console.log(neighborList);
				}
					
				// set active nodes
				
				nodes.each(function(p) {
					var j = nodeNeighbors.nodes.indexOf(p);
					d3.select(this)
					.transition()
					.duration(duration)
					.style('r', j == 0? 25: r)
					.style("opacity", j > -1 ? 1 : .25)
					.style("stroke-width", j > -1 ? 3 : 1)
					.style("stroke", j > -1 ? "blue" : "white")
				});
				// set active edges
				links.each(function(l, idx) {
					var j = nodeNeighbors.links.indexOf(l);
					d3.select(this)
					.transition()
					.duration(duration)
					.style("opacity", j > -1 ? 1 : .25)
					.style("stroke-width", j > -1 ? 2 : 1)
					.style("stroke", j > -1 ? "black" : defaultColor)
					.style('marker-end', j > -1? 'url(#arrowhead1)':'url(#arrowhead)' )
				});	
				// set active node labels
				nodelabels.each(function(p, idx){
					var j = nodeNeighbors.nodeIdx.indexOf(idx);
					d3.select(this)
					.transition()
					.duration(duration)					
					.style("opacity", j > -1 ? 1 : .25)
					.style("font-size", j > -1 ? 20 : fontSize)
				});
				// set active edge labels
				edgelabels.each(function(p, idx){
					var j = nodeNeighbors.linkIdx.indexOf(idx);
					d3.select(this)
					.transition()
					.duration(duration)	
					.style("stroke", j > -1 ? "black" : defaultColor)
					.style("opacity", j > -1 ? 1 : .25)
					//.style("font-size", j > -1 ? 20 : 15)
				})
				
			}
			 
			function findNeighbors(d) {
				var neighborArray = [d];
				var linkArray = [];
				var neighborIdx = [d.index];
				var linkIdx = [];
				links.each(function(l, idx) {
					if(l.source == d && l.source != l.target){
						neighborArray.indexOf(l.target) == -1 ? neighborArray.push(l.target) && neighborIdx.push(l.target.index) && linkArray.push(l) && linkIdx.push(idx): null;			
					}
					if(l.target == d && l.source != l.target){
						neighborArray.indexOf(l.source) == -1 ? neighborArray.push(l.source) && neighborIdx.push(l.source.index) && linkArray.push(l) && linkIdx.push(idx): null;
					}
				})
				
				dic = {nodes: neighborArray, links: linkArray, nodeIdx: neighborIdx, linkIdx: linkIdx}
				//console.log(dic)
				return dic;
			} 
			
			var mouseover = function(d, i) {
			  highlightNeighbors(d, i);
			}
			
			nodes.on('mouseover', mouseover);
			
			var mouseout = function() {
			
			    d3.selectAll('circle')
			  		.transition()
					.duration(duration)
					.style('r', r)
					.style("opacity", 1)
					.style("stroke-width", 1)
					.style("stroke", "white");
				d3.selectAll('line')
					.transition()
					.duration(duration)
					.style("opacity", 1)
					.style("stroke-width", 1)
					.style("stroke", defaultColor)
					.style('marker-end', 'url(#arrowhead)' );
				d3.selectAll('.nodelabel')
					.transition()
					.duration(duration)					
					.style("opacity", 1)
					.style("font-size", fontSize);
				d3.selectAll('.edgelabel')
					.transition()
					.duration(duration)	
					.style("stroke",  defaultColor)
					.style("opacity", 1)
			}
			
			nodes.on('mouseout', mouseout);

			force.on("tick", function(){

				links.attr({"x1": function(d){return d.source.x;},
							"y1": function(d){return d.source.y;},
							"x2": function(d){return d.target.x;},
							"y2": function(d){return d.target.y;}
				});

				nodes.attr({"cx":function(d){return d.x;},
							"cy":function(d){return d.y;}
				});

				nodelabels.attr("x", function(d) { return d.x; }) 
						  .attr("y", function(d) { return d.y; });

				edgepaths.attr('d', function(d) { var path='M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y;
												   //console.log(d)
												   return path});       


			});
	}