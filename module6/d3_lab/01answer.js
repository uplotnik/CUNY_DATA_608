d3.csv(''https://github.com/uplotnik/CUNY_DATA_608/blob/master/module6/d3_lab/ue_industry.csv', data => {

    // Define your scales and generator here.
  console.log(data);

    
    const xScale = d3.scaleLinear()
        .domain(d3.extent(data, d => +d.index))
        .range([1190, 25]);
    
    const yScale = d3.scaleLinear()
        .domain(d3.extent(data, d => +d.Agriculture))
        .range([570, 18]);
    
    let line10 = d3.line()
        .x(d => xScale(d.index))
        .y(d => yScale(d.Agriculture));
    
d3.select('#answer1')
        // append more elements here
      .selectAll('path')
        .data(data)
        .enter()        
        .append('path')
        .attr('d', line10(data))
        .attr("stroke-width", 1.8)
        .attr("stroke", "darkblue")
});
