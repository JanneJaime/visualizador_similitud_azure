function showGrafo(){
    $('#main').hide();
    $('#secondary').show();
    $('#searchbox').removeClass('container')
                    .addClass('navbar')
                    .addClass('navbar-expand-sm')
                    .addClass('bg-light')
                    .addClass('navbar-light')
                    .addClass('sticky-top');
    $('<div style="height:60px;"><p></p></div>').insertBefore("#searchbox" );
    $('#searchbox').css({"margin-top":"", "top":"10%", "padding-top":"15px"});
        
}
let values = {
    nodes:[],
    links: []
};
var svg = d3.select('svg').style("font", "12px sans-serif");
var width = 100;
var height = svg.attr("height");
svg.attr("viewBox", [-width / 2, - (height-100) / 2, width, height]);
var r = 30;

var simulation;
var link = svg;
var node = svg;

var Tooltip = d3.select("#graph")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "aliceblue")
    .style("border", "solid")
    .style("border-width", "2px")
    .style("border-radius", "5px")
    .style("max-width", "250px")
    .style("padding", "5px")

function loadGrafo(resp){
    resp.grafos.nodos.forEach(e => {
        values.nodes.push({'name':e.id,'title':e.title})
    });
    resp.grafos.enlaces.forEach(e => {
        values.links.push({source:e.source,target:e.target})
    });
    

    simulation = d3
        .forceSimulation(values.nodes)
        .force("link",d3.forceLink()
            .id(function(d){return d.name;})
            .links(values.links))
        .force("charge",d3.forceManyBody().strength(-400))    
        .force("x",d3.forceX())
        .force("y",d3.forceY())
        .force("collide",d3.forceCollide(r+20))    
        .on("tick",ticked);
    
    
    link = svg
        .append("g")
        .selectAll("line")
        .data(values.links)
        .enter()
        .append("line")
        .attr("stroke-width",3)
        .attr("stroke","black")
    
    var drag = d3
        .drag()
        .on("start",dragstarted)
        .on("drag",dragged)
        .on("end",dragended);
    
    // var node = svg
    //     .append("g")
    //     .selectAll("g")
    //     .data(values.nodes)
    //     .enter()
    //     .append("g")
    
    node = svg
        .append("g")
        .attr("fill", "currentColor")
        .attr("stroke-linecap", "round")
        .attr("stroke-linejoin", "round")
      .selectAll("g")
      .data(values.nodes)      
      .join("g")
        .on("mouseover", mouseover)
        .on("mousemove", mousemove)
        .on("mouseleave", mouseleave)
        .call(drag);
    
    node.append("circle")
        .attr("stroke", "black")
        .attr("stroke-width", 1.5)
        .attr("fill","#7FB3D5")
        .attr("r", d => Math.random()*2+r);
    
    node.append("text")
        .attr("x", -r/2)
        .attr("y", "0.31em")
        .attr("color","white")
        .attr("font-weight","bold")
        .text(d => d.name)
      .clone(true).lower()
        .attr("fill", "none")
        .attr("stroke", "white")
        .attr("stroke-width", 3);
    

}

function ticked(){
    link
        .attr("x1",function(d){return d.source.x})
        .attr("y1",function(d){return d.source.y})
        .attr("x2",function(d){return d.target.x})
        .attr("y2",function(d){return d.target.y})

    // node
    //     .attr("cx",function(d){return d.x;})
    //     .attr("cy",function(d){return d.y;})
    node.attr("transform", d => `translate(${d.x},${d.y})`);
}
function dragstarted(d){
    simulation.alphaTarget(0.3).restart();
    d.subject.fx = d.subject.fx;
    d.subject.fy = d.subject.fy;
}
function dragged(d){
    d.subject.fx = d.x;
    d.subject.fy = d.y;
}
function dragended(d){
    simulation.alphaTarget(0);
    d.subject.fx = null;
    d.subject.fy = null;
}
function mouseover(event,d) {
    $(`#${d.name}`).css('background-color','#7FD6DD').focus();
    // $('#searchbox').hide();
    // window.location.href =`#${d.name}`;
    Tooltip
      .style("opacity", 1)
    
    
  }
function mousemove(event,d) {
    Tooltip
        .html("Titulo: " + d.title)
        .style("left", (window.scrollX+d3.pointer(event)[0]) + "px")
        .style("top", (window.scrollY+d3.pointer(event)[1]) + "px")
}
function mouseleave(event,d) {
    // $('#searchbox').show();
    
    $(`#${d.name}`).css('background-color','white')
    Tooltip
        .style("opacity", 0)

}