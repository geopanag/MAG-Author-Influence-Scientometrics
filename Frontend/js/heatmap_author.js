
function get_author_frontier(){

  	var author = document.getElementById('coords').value;
  	var author_name = document.getElementById('author_name').value;
	  var type_author = document.getElementById('type').value;

  	// $("#my_heatmap").empty();
  	document.getElementById("my_heatmap").innerHTML = '';

	author_split = author.split(",");

	// set the dimensions and margins of the graph
	var margin = {top: 35, right: 25, bottom: 60, left: 60},
	  width = 800 - margin.left - margin.right,
	  height = 601 - margin.top - margin.bottom;


	// append the svg object to the body of the page
	var svg = d3.select("#my_heatmap")
	.append("svg")
	  .attr("width", width + margin.left + margin.right)
	  .attr("height", height + margin.top + margin.bottom)
	  .append("g")
	  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	//Read the data
	// d3.csv("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/heatmap_data.csv", function(data) {
	if (type_author === 0 || type_author==="0") {
  	  var step = 100;
  	  var denom = 1;
  	  var file_name = "dcore_image_100.csv";
  	  // var maxc = 7000000;
      var maxc = 200000;
	}else{
  	  var step = 78;
  	  var denom = 100;
  	  var file_name = "dcore_image_r.csv";
  	  var maxc = 20000;
	}


	  d3.csv(file_name, function(data) {

  	  var arrayLength = author_split.length;

  	  // show the frontier
  	  // for coord in author_split{

  	  var maxy = 0;
  	  var maxx = 0;
  	  for (var i = 0; i < arrayLength; i++) {
  	    // coordy_in = Math.floor(parseInt(author_split[i].split('#')[0],10));
  	    // coordx_out = Math.floor(parseInt(author_split[i].split('#')[1],10));
  	    coordy_in = Math.floor(parseInt(author_split[i].split('#')[0]));
  	    coordx_out = Math.floor(parseInt(author_split[i].split('#')[1]));

  	    // iterate over each element in the array
  	    for (var j = 0; j < data.length; j++){
  	      // look for the entry with a matching code` value
  	      if (data[j].group == coordx_out && data[j].variable == coordy_in){
  	         data[j].value = 0;
  	         // break;
  	      }
  	    }

  	    if(coordx_out>=maxx && coordy_in>=maxy){
  	    	maxy = coordy_in;
  	    	maxx = coordx_out;
  	    }
  	  }

  	   for (var maxx_i=maxx-1; maxx_i>=0; maxx_i--){
  	    // iterate in y until you find the maximum y
    		for (var j = 0; j < data.length; j++){
    		   	if(data[j].variable==maxy && data[j].group==maxx_i){
    		   		temp = 0;
    		   		for(var k=j; k<j+step-(maxy/denom); k++){//look until the maximum
    		   		   	if(data[k].value == 0){
    		   		   		temp = data[k].variable; //keep the final frontier
    		   		   	}
    		   		}
    		   		if(temp==0){
    		   			data[j].value = 0; //if nothing is found, this is the next frontier
    		   		}else{
    		   			maxy = temp;//update next rectangle
    		   		}
    		  	}
    		 }
  	   }


  	  // Labels of row and columns -> unique identifier of the column called 'group' and 'variable'
  	  var myGroups = d3.map(data, function(d){return d.group;}).keys()
  	  var myVars = d3.map(data, function(d){return d.variable;}).keys()
  	  var valuesd = d3.map(data, function(d){return d.value;}).keys()

  	  // Build X scales and axis:
  	  var x = d3.scaleBand()
  	    .range([ 0, width ])
  	    .domain(myGroups)
  	    .padding(0.05);

      var xax = d3.scaleLinear()
        .domain([0, Math.max.apply(Math,myGroups)])
        .range([ 0, width ]);

  	  svg.append("g")
  	    .style("font-size", 10)
  	    .attr("transform", "translate(0," + 0 + ")")
  	    .call(d3.axisTop(xax).tickSize(0))
  	    .select(".domain").remove()

  	// text label for the x axis
    	svg.append("text")
        .attr("transform", "translate(" + (width/2) + " ," + -20 + ")")
        .style("text-anchor", "middle")
        .text("Out degree");

  	  // Build Y scales and axis:
  	  var y = d3.scaleBand()
  	    .range([ 0, height, 10 ])
  	    .domain(myVars)
  	    .padding(0.05);

      var yax = d3.scaleLinear()
        .domain([0, Math.max.apply(Math,myVars)])
        .range([0, height]);

  	  svg.append("g")
  	    .style("font-size", 10)
  	    .call(d3.axisLeft(yax).tickSize(0))
        .select(".domain").remove()

  	 // text label for the y axis
    	svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("In degree");

  	  var myColor = d3.scaleSequential(d3.interpolateBlues)
      	.domain([1,maxc]);//Math.max.apply(Math,valuesd)

  	  // create a tooltip
  	  var tooltip = d3.select("#my_heatmap")
  	    .append("div")
  	    .style("opacity", 0)
  	    .attr("class", "tooltip")
  	    .style("background-color", "white")
  	    .style("border", "solid")
  	    .style("border-width", "1px")
  	    .style("border-radius", "1px")
  	    .style("padding", "1px")

  	  // Three function that change the tooltip when user hover / move / leave a cell
  	  var mouseover = function(d) {
  	    tooltip
  	      .style("opacity", 1)
  	    d3.select(this)
  	      .style("stroke", "black")
  	      .style("opacity", 1)
  	  }
  	  var mousemove = function(d) {
  	    tooltip
  	      .html("Number of authors<br>in dcore: " + d.value)
  	      .style("left", (d3.mouse(this)[0]+70) + "px")
  	      .style("top", (d3.mouse(this)[1]) + "px")
  	  }

  	   var mouseleave = function(d) {
	    tooltip
	      .style("opacity", 0)
	    d3.select(this)
	      .style("stroke", "none")
	      .style("opacity", 0.8)
	  }

	  svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 + height + 15 )
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "underline")
        .text(author_name);
  	  // show the frontier
  	  // for coord in author_split{

    // add the squares
	  svg.selectAll()
	    .data(data, function(d) {return d.group+':'+d.variable;})
	    .enter()
	    .append("rect")
	      .attr("x", function(d) { return x(d.group) })
	      .attr("y", function(d) { return y(d.variable) })
	      .attr("rx", 4)
	      .attr("ry", 4)
	      .attr("width", x.bandwidth() )
	      .attr("height", y.bandwidth() )
	      // .style("fill", function(d) { return myColor(1-Math.exp(-d.value))} )
	      .style("fill", function(d) { return myColor(d.value)} )
	      .style("stroke-width", 4)
	      .style("stroke", "none")
	      .style("opacity", 0.8)
	    .on("mouseover", mouseover)
	    .on("mousemove", mousemove)
	    .on("mouseleave", mouseleave)
	})


}
