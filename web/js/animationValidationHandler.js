// transition to dynamic display and halt:
$( document ).ready(function() {
    $('.hud').one("animationend", function(){
        setTimeout(function() {
          // now start adding the dropdown.
          addDropButtons();
          // $('#container').remove(); use this to remove
        }, 0);
      }
    );
});

//---------------------------------------------------------------------------------------------------
//  functional methods here:
var textValidationType;
var textPlateType
var textQuadrantSplitType;
var filePath;
var mapInput;
var controlAndNaNWells = ["A1", "B1", "C1", "D1", "E11", "F11", "G11", "H11",
                        "A12", "B12", "C12", "D12", "E12", "F12", "G12", "H12"];

//---------------------------------------------------------------------------------------------------
function initialPlateMap(){
  // Deletes previous plate if exist
//  d3.select("#inputPlate").selectAll('svg').remove();
  $("#inputPlate").empty()
  // Labels of row and columns and size of the SVG
  var rows = ["A", "B", "C", "D", "E", "F", "G", "H"];
  var columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];
  var margin = {top: 30, right: 30, bottom: 30, left: 30};
  var width = (125 * 5) - margin.left - margin.right;
  var height = (82 * 5) - margin.top - margin.bottom;

  // SVG template
  var svg = d3.select("#inputPlate")
                .append("svg")
                .attr("id", "inGridSvg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("id", "inGrid")
                .attr("transform", "translate("+margin.left+","+margin.top+")");


  // you have to have an x and y variable for array/ matrices.
  // Build X scales and axis:
  var x = d3.scaleBand() // just a scale
              .domain(columns) // represents matrix location
              .range([0, width])
              .padding(0.01)


  // Build Y scales and axis:
  var y = d3.scaleBand() // just a scale
              .domain(rows) // domain is 8, represents matrix location
              .range([0, height]) // divides domain up by this much?
              .padding(0.01)

  // SVG generate X axis
  // svg.append("g").attr("transform", "translate(0,"+height+")").call(d3.axisBottom(x));
  svg.append("g")
            .attr("transform", "translate(0, -2)") // this was for the distance between the axis line
            .call(d3.axisTop(x).tickSize([0, 0]))
            .call(g => g.select(".domain").remove()) // to remove the ticks (lines of the ticks)
            .attr("class", "axis");
  // SVG generate Y axis
  svg.append("g")
            .attr("transform", "translate(-2, 0)")
            .call(d3.axisLeft(y).tickSize([0, 0]))
            .call(g => g.select(".domain").remove())
            .attr("class", "axis");

  //Read the data

  for(var columnCount=0; columnCount<12; columnCount++){
    for(var rowCount=0; rowCount<8; rowCount++){
      var idWell = rows[rowCount] + columns[columnCount]
      if (!controlAndNaNWells.includes(idWell)){
      d3.select("#inGrid")
            .append("rect").on("click", function(){changeWellColor($(this).attr("id"))})
            .attr("x", function() { return x(columns[columnCount]) }) // x(columns[columnCount]). inputting columns[columnCount] into var x which is a built in function of d3.
            // var x is now being sliced by columns[columnCount] with this function x.
            // "x" is a css attribute.
            .attr("y", function() { return y(rows[rowCount]) })
            // var y is now being sliced by columns[columnCount] with this function y.
            // "y" is a css attribute.
            .attr("id", idWell)
            .attr("width", x.bandwidth() ) // bandwidth is a d3 function where it automatically centers axis with cell.
            .attr("height", y.bandwidth() ) // the length of size (170px) variable divided by domain (ex 8 rows).
            .attr("style","fill:white;stroke:black;stroke-width:2")
          }
      else{
        d3.select("#inGrid")
              .append("rect")//.on("click", function(){changeWellColor($(this).attr("id"))})
              .attr("x", function() { return x(columns[columnCount]) }) // x(columns[columnCount]). inputting columns[columnCount] into var x which is a built in function of d3.
              // var x is now being sliced by columns[columnCount] with this function x.
              // "x" is a css attribute.
              .attr("y", function() { return y(rows[rowCount]) })
              // var y is now being sliced by columns[columnCount] with this function y.
              // "y" is a css attribute.
              .attr("id", idWell)
              .attr("width", x.bandwidth() ) // bandwidth is a d3 function where it automatically centers axis with cell.
              .attr("height", y.bandwidth() ) // the length of size (170px) variable divided by domain (ex 8 rows).
              .attr("style","fill:grey;stroke:black;stroke-width:2")
      }
    }
  }
}

// #############################################################################################################################
function makeQuadPlateMap(className, quadNum){
  // Labels of row and columns and size of the SVG
  var rows = ["A", "B", "C", "D", "E", "F", "G", "H"];
  var columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];
  var margin = {top: 30, right: 30, bottom: 30, left: 30};
  var width = (125 * 5) - margin.left - margin.right;
  var height = (82 * 5) - margin.top - margin.bottom;

  // SVG template
  var svg = d3.select(className)
                .append("svg")
                .attr("id", "inGridSvg" + quadNum)
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("id", "inGrid" + quadNum)
                .attr("transform", "translate("+margin.left+","+margin.top+")");


  // you have to have an x and y variable for array/ matrices.
  // Build X scales and axis:
  var x = d3.scaleBand() // just a scale
              .domain(columns) // represents matrix location
              .range([0, width])
              .padding(0.01)


  // Build Y scales and axis:
  var y = d3.scaleBand() // just a scale
              .domain(rows) // domain is 8, represents matrix location
              .range([0, height]) // divides domain up by this much?
              .padding(0.01)

  // SVG generate X axis
  // svg.append("g").attr("transform", "translate(0,"+height+")").call(d3.axisBottom(x));
  svg.append("g")
            .attr("transform", "translate(0, -2)") // this was for the distance between the axis line
            .call(d3.axisTop(x).tickSize([0, 0]))
            .call(g => g.select(".domain").remove()) // to remove the ticks (lines of the ticks)
            .attr("class", "axis");
  // SVG generate Y axis
  svg.append("g")
            .attr("transform", "translate(-2, 0)")
            .call(d3.axisLeft(y).tickSize([0, 0]))
            .call(g => g.select(".domain").remove())
            .attr("class", "axis");

  $(className).append($("<h5/>").html("Quadrant " + quadNum).attr({"style": "text-align: center;"}))
  //Read the data

  for(var columnCount=0; columnCount<12; columnCount++){
    for(var rowCount=0; rowCount<8; rowCount++){
      var idWell = rows[rowCount] + columns[columnCount]
      if (!controlAndNaNWells.includes(idWell)){
      d3.select("#inGrid" + quadNum)
            .append("rect").on("click", function(){changeWellColor384($(this).attr("id"), $(this).attr("class"))})
            .attr("x", function() { return x(columns[columnCount]) }) // x(columns[columnCount]). inputting columns[columnCount] into var x which is a built in function of d3.
            // var x is now being sliced by columns[columnCount] with this function x.
            // "x" is a css attribute.
            .attr("y", function() { return y(rows[rowCount]) })
            // var y is now being sliced by columns[columnCount] with this function y.
            // "y" is a css attribute.
            .attr("id", idWell)
            .attr("class", "quad" + quadNum)
            .attr("width", x.bandwidth() ) // bandwidth is a d3 function where it automatically centers axis with cell.
            .attr("height", y.bandwidth() ) // the length of size (170px) variable divided by domain (ex 8 rows).
            .attr("style","fill:white;stroke:black;stroke-width:2")
          }
      else{
        d3.select("#inGrid" + quadNum)
              .append("rect")//.on("click", function(){changeWellColor($(this).attr("id"))})
              .attr("x", function() { return x(columns[columnCount]) }) // x(columns[columnCount]). inputting columns[columnCount] into var x which is a built in function of d3.
              // var x is now being sliced by columns[columnCount] with this function x.
              // "x" is a css attribute.
              .attr("y", function() { return y(rows[rowCount]) })
              // var y is now being sliced by columns[columnCount] with this function y.
              // "y" is a css attribute.
              .attr("id", idWell)
              .attr("class", "quad" + quadNum)
              .attr("width", x.bandwidth() ) // bandwidth is a d3 function where it automatically centers axis with cell.
              .attr("height", y.bandwidth() ) // the length of size (170px) variable divided by domain (ex 8 rows).
              .attr("style","fill:grey;stroke:black;stroke-width:2")
      }
    }
  }
}


function initialPlateMap384(){
  $("#inputPlate").empty()
  $("#inputPlate").append($("<div/>").addClass("carousel slide").attr({"id": "AccurMapCarouselIndicators", "data-ride":"carousel"})
                    .append($("<ol/>").addClass("carousel-indicators")
                                      .append($("<li/>").addClass("active").attr({"data-target":"AccurMapCarouselIndicators", "data-slide-to": "0"}))
                                      .append($("<li/>").attr({"data-target":"AccurMapCarouselIndicators", "data-slide-to": "1"}))
                            )
                    .append($("<div/>").addClass("carousel-inner")
                                       .append($("<div/>").addClass("carousel-item active map1")
                                                          .append($("<div/>").addClass("tooltip")))
                                       .append($("<div/>").addClass("carousel-item map2")
                                                          .append($("<div/>").addClass("tooltip")))
                                       .append($("<div/>").addClass("carousel-item map3")
                                                          .append($("<div/>").addClass("tooltip")))
                                       .append($("<div/>").addClass("carousel-item map4")
                                                          .append($("<div/>").addClass("tooltip")))
                           )
                    .append($("<a/>").addClass("icon384map carousel-control-prev").attr({"href":"#AccurMapCarouselIndicators", "role":"button", "data-slide":"prev"})
                                     .append($("<span/>").addClass("icon384map carousel-control-prev-icon").attr({"aria-hidden": "true"}))
                           )
                    .append($("<a/>").addClass("icon384map carousel-control-next").attr({"href":"#AccurMapCarouselIndicators", "role":"button", "data-slide":"next"})
                                      .append($("<span/>").addClass("icon384map carousel-control-next-icon").attr({"aria-hidden": "true"}))
                           )
                          )

  makeQuadPlateMap(".map1", 1)
  makeQuadPlateMap(".map2", 2)
  makeQuadPlateMap(".map3", 3)
  makeQuadPlateMap(".map4", 4)
}

function changeWellColor384(wellPosID, className){
              console.log(wellPosID)
              console.log(className)


              var currentColor = d3.select("." + className + "#" + wellPosID).style('fill')
              console.log(currentColor)

              if (currentColor == "white"){
                d3.select("." + className + "#" + wellPosID).style("fill", "black");
              }
              else if (currentColor == "black"){
                d3.select("." + className + "#" + wellPosID).style("fill", "red");
              }
              else if (currentColor == "red"){
                d3.select("." + className + "#" + wellPosID).style("fill", "blue");
              }
              else if (currentColor == "blue"){
                d3.select("." + className + "#" + wellPosID).style("fill", "green");
              }
              else if (currentColor == "green"){
                d3.select("." + className + "#" + wellPosID).style("fill", "white");
              }
}

function changeWellColor(wellPosID){ //, rowCount, columnCount){
              var currentColor = d3.select("#" + wellPosID).style('fill')

              if (currentColor == "white"){
                d3.select("#" + wellPosID).style("fill", "black");
              }
              else if (currentColor == "black"){
                d3.select("#" + wellPosID).style("fill", "red");
              }
              else if (currentColor == "red"){
                d3.select("#" + wellPosID).style("fill", "blue");
              }
              else if (currentColor == "blue"){
                d3.select("#" + wellPosID).style("fill", "green");
              }
              else if (currentColor == "green"){
                d3.select("#" + wellPosID).style("fill", "white");
              }
}

//---------------------------------------------------------------------------------------------------
async function compareMapButton(){
  var rows = ["A", "B", "C", "D", "E", "F", "G", "H"];
  var columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];

  var negCount = 0
  var cps100Count = 0
  var cps200Count = 0
  var cps2000Count = 0
  var cps20000Count = 0
  var plateMapColorArray = new Array(96);

  $("#inGridSvg rect").each( function( index, element){ // included #inGridSvg
     // console.log(index, $(element));
     // d3.select("#" + wellPosID).style('fill')
     concentrationOfSpike = d3.select("#" + $(element).attr("id")).style('fill');
     if(!controlAndNaNWells.includes($(element).attr("id"))){
       if (concentrationOfSpike == "white"){
         plateMapColorArray[index] = "neg";
         negCount += 1;
       }
       else if (concentrationOfSpike == "black"){
         plateMapColorArray[index] = 100;
         cps100Count += 1;
       }
       else if (concentrationOfSpike == "red"){
         plateMapColorArray[index] = 200;
         cps200Count += 1;
       }
       else if (concentrationOfSpike == "blue"){
         plateMapColorArray[index] = 2000;
         cps2000Count += 1;
       }
       else if (concentrationOfSpike == "green"){
         plateMapColorArray[index] = 20000;
         cps20000Count += 1;
       }
     }
     else if(index < 4){
       plateMapColorArray[index] = "control";
     }
     else{
       plateMapColorArray[index] = "N/A";
     }
  });

  if (negCount == 30 && cps100Count == 20 && cps200Count == 20 && cps2000Count == 5 && cps20000Count == 5){
    console.log("Pass that data.", negCount, cps100Count, cps200Count, cps2000Count, cps20000Count)
    let dataFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath, plateMapColorArray)();

    let sarsDfasObj = JSON.parse(dataFromPython[0]);
    let calRedDfasObj = JSON.parse(dataFromPython[1]);
    let outputAccuracySummaryString = dataFromPython[2]
    let platePassed = dataFromPython[3]

    console.log(sarsDfasObj)
    console.log(calRedDfasObj)
    console.log(outputAccuracySummaryString)
    console.log(platePassed)

    if (!jQuery.isEmptyObject(sarsDfasObj)){
      makeOutputHeatMap(sarsDfasObj, ".sarsDivPlacement", "heatMapGrid", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
    }
    if (!jQuery.isEmptyObject(calRedDfasObj)){
      makeOutputHeatMap(calRedDfasObj, ".calRedDivPlacement", "heatMapGrid2", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
    }
    $('#inputMapModal').modal("hide")
  }
  else{
    console.log("Dont pass that data.", negCount, cps100Count, cps200Count, cps2000Count, cps20000Count)
  }
}
// ##############################################################################

async function compareMapButton384(quadrantSplit){ ////
  let grid = ["#inGridSvg1", "#inGridSvg2", "#inGridSvg3", "#inGridSvg4"]
  let plateMapColorArray384 = new Array(4);
  let passData = true

  for(var i = 0; i < grid.length; i++){
    console.log(grid[i])
    let negCount = 0
    let cps100Count = 0
    let cps200Count = 0
    let cps2000Count = 0
    let cps20000Count = 0
    let plateMapColorArray = new Array(96);

    $(grid[i] + " rect").each(function( index, element){ // included #inGridSvg
       concentrationOfSpike = d3.select("." + $(this).attr("class") + "#" + $(element).attr("id")).style('fill');
       if(!controlAndNaNWells.includes($(element).attr("id"))){
         if (concentrationOfSpike == "white"){
           plateMapColorArray[index] = "neg";
           negCount += 1;
         }
         else if (concentrationOfSpike == "black"){
           plateMapColorArray[index] = 100;
           cps100Count += 1;
         }
         else if (concentrationOfSpike == "red"){
           plateMapColorArray[index] = 200;
           cps200Count += 1;
         }
         else if (concentrationOfSpike == "blue"){
           plateMapColorArray[index] = 2000;
           cps2000Count += 1;
         }
         else if (concentrationOfSpike == "green"){
           plateMapColorArray[index] = 20000;
           cps20000Count += 1;
         }
       }
       else if(index < 4){
         plateMapColorArray[index] = "control";
       }
       else{
         plateMapColorArray[index] = "N/A";
       }
    });

    if (negCount == 30 && cps100Count == 20 && cps200Count == 20 && cps2000Count == 5 && cps20000Count == 5){
      console.log("Pass that data.", negCount, cps100Count, cps200Count, cps2000Count, cps20000Count)
      plateMapColorArray384[i] = plateMapColorArray
    }
    else{
      console.log("Don't pass that data.", negCount, cps100Count, cps200Count, cps2000Count, cps20000Count)
      passData = false
    }
  }

  if (passData == true) {
    // pass 384 data with eel.
    console.log(plateMapColorArray384)
    if (quadrantSplit = false) {
      let dataFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath, plateMapColorArray384)();
      let sarsDfasObj = JSON.parse(dataFromPython[0]);
      let calRedDfasObj = JSON.parse(dataFromPython[1]);
      let outputAccuracySummaryString = dataFromPython[2]
      let platePassed = dataFromPython[3]

      if (!jQuery.isEmptyObject(sarsDfasObj)){
        makeOutputHeatMap384(sarsDfasObj, ".sarsDivPlacement", "heatMapGrid", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
      }
      if (!jQuery.isEmptyObject(calRedDfasObj)){
        makeOutputHeatMap384(calRedDfasObj, ".calRedDivPlacement", "heatMapGrid2", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
      }
   }
   else {
     let dataFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath, plateMapColorArray384)();
     let sarsDfasObjQuads = [JSON.parse(dataFromPython[0]), JSON.parse(dataFromPython[1]), JSON.parse(dataFromPython[2]), JSON.parse(dataFromPython[3])]
     let calRedDfasObjQuads = [JSON.parse(dataFromPython[4]), JSON.parse(dataFromPython[5]), JSON.parse(dataFromPython[6]), JSON.parse(dataFromPython[7])]
     let outputAccuracySummaryString = [dataFromPython[8], dataFromPython[9], dataFromPython[10], dataFromPython[11]]
     let platePassed = [dataFromPython[12], dataFromPython[13], dataFromPython[14], dataFromPython[15]]

     addPageNav2HeatMapCarousel(sarsDfasObjQuads, calRedDfasObjQuads, outputAccuracySummaryString, platePassed)
   }
    $('#inputMapModal').modal("hide")
  }

}

// ##############################################################################
function makeOutputHeatMap(sarsDfasObj, divPlacement, heatMapID, outputAccuracySummaryString, platePassed){
    $(divPlacement).empty()

    let rows = ["A", "B", "C", "D", "E", "F", "G", "H"];
    let columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];
    let margin = {top: 30, right: 30, bottom: 30, left: 30};
    let width = (125 * 5) - margin.left - margin.right;
    let height = (82 * 5) - margin.top - margin.bottom;

    let svg = d3.select(divPlacement) // .calRedDivPlacement
            .append("svg")
            .attr("id", "heatMapSvg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("id", heatMapID) // #heatMapGrid2
            .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");


          // you have to have an x and y variable for array/ matrices.
          // Build X scales and axis:
          let x = d3.scaleBand() // just a scale
                      .domain(columns) // represents matrix location
                      .range([0, width])
                      .padding(0.01)


          // Build Y scales and axis:
          let y = d3.scaleBand() // just a scale
                      .domain(rows) // domain is 8, represents matrix location
                      .range([0, height]) // divides domain up by this much?
                      .padding(0.01)


          // SVG generate X axis
          // svg.append("g").attr("transform", "translate(0,"+height+")").call(d3.axisBottom(x));
          svg.append("g")
                    .attr("transform", "translate(0, -2)") // this was for the distance between the axis line
                    .call(d3.axisTop(x).tickSize([0, 0]))
                    .call(g => g.select(".domain").remove()) // to remove the ticks (lines of the ticks)
                    .attr("class", "axis");
          // SVG generate Y axis
          svg.append("g")
                    .attr("transform", "translate(-2, 0)")
                    .call(d3.axisLeft(y).tickSize([0, 0]))
                    .call(g => g.select(".domain").remove())
                    .attr("class", "axis");

          let heatColor;
          if (divPlacement == ".calRedDivPlacement"){
                $(divPlacement).append($("<h5/>").html("Human CT Heatmap").attr({"style": "text-align: center;"}))
                // Build color scale
                heatColor = d3.scaleLinear()
                  .range(["blue", "white"])
                  .domain([45, 20]) // fix to max and min
              }
          else{
                $(divPlacement).append($("<h5/>").html("SARS CT Heatmap").attr({"style": "text-align: center;"}))
                // Build color scale
                heatColor = d3.scaleLinear()
                  .range(["red", "white"])
                  .domain([45, 10]) // fix to max and min
              }

          if (platePassed){
              $(divPlacement).append($("<p/>").html(outputAccuracySummaryString).attr({"style": "text-align: center; display:inline-block;width: 58%; margin: 0% 21% 0% 21%; color: green"}))
          }
          else{
            $(divPlacement).append($("<p/>").html(outputAccuracySummaryString).attr({"style": "text-align: center; display:inline-block;width: 58%; margin: 0% 21% 0% 21%; color: red"}))
          }

            //Read the data
                for (var columnCount = 1; columnCount <= 12; columnCount++) {
                  for (var rowCount = 0; rowCount < 8; rowCount++) {
                    d3.select("#"+heatMapID).selectAll("wellPositions") //heatMapGrid2
                      .data([sarsDfasObj])
                      .enter()
                      .append("rect")
                      .attr("x", function() {
                        return x(columnCount)
                      })
                      .attr("y", function(d) {
                        return y(rows[rowCount])
                      })
                      .attr("width", x.bandwidth())
                      .attr("height", y.bandwidth())
                      .attr("style", "stroke:black;stroke-width:2")
                      .style("fill", function(d) {
                        // if (d[columnCount][rows[rowCount]] >= 40) {
                        if (d[columnCount][rows[rowCount]] >= 40 || d[columnCount][rows[rowCount]] == null) {
                          // return heatColor(null)
                          return "white"
                        } else {
                          return heatColor(d[columnCount][rows[rowCount]])
                        }
                      })

                   d3.select("#"+heatMapID).selectAll()
                      .data([sarsDfasObj])
                      .enter()
                      .append("text")
                      .text(function(d){
                        if (d[columnCount][rows[rowCount]] != null){
                          return Math.round(d[columnCount][rows[rowCount]]* 100) / 100
                        }
                        return d[columnCount][rows[rowCount]]
                      })
                      .attr("x", function() {
                        return x(columnCount) + 4;
                      })
                      .attr("y", function(d) {
                        return y(rows[rowCount]) + 29;
                      })
                      .attr("style", "font-size: 14px;")
                  }
            }
}

function makeOutputHeatMap384(sarsDfasObj, divPlacement, heatMapID, outputAccuracySummaryString, platePassed){
    $(divPlacement).empty()
    // $('.pageNavQuads').empty()

    let rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"];
    let columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12",
                  "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"];
    let margin = {top: 30, right: 30, bottom: 30, left: 30};
    let width = (125 * 5) - margin.left - margin.right;
    let height = (82 * 5) - margin.top - margin.bottom;

    let svg = d3.select(divPlacement) // .calRedDivPlacement
            .append("svg")
            .attr("id", "heatMapSvg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("id", heatMapID) // #heatMapGrid2
            .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");


          // you have to have an x and y variable for array/ matrices.
          // Build X scales and axis:
          let x = d3.scaleBand() // just a scale
                      .domain(columns) // represents matrix location
                      .range([0, width])
                      .padding(0.01)


          // Build Y scales and axis:
          let y = d3.scaleBand() // just a scale
                      .domain(rows) // domain is 8, represents matrix location
                      .range([0, height]) // divides domain up by this much?
                      .padding(0.01)


          // SVG generate X axis
          // svg.append("g").attr("transform", "translate(0,"+height+")").call(d3.axisBottom(x));
          svg.append("g")
                    .attr("transform", "translate(0, -2)") // this was for the distance between the axis line
                    .call(d3.axisTop(x).tickSize([0, 0]))
                    .call(g => g.select(".domain").remove()) // to remove the ticks (lines of the ticks)
                    .attr("class", "axis");
          // SVG generate Y axis
          svg.append("g")
                    .attr("transform", "translate(-2, 0)")
                    .call(d3.axisLeft(y).tickSize([0, 0]))
                    .call(g => g.select(".domain").remove())
                    .attr("class", "axis");

          let heatColor;
          if (divPlacement == ".calRedDivPlacement"){
                $(divPlacement).append($("<h5/>").html("Human CT Heatmap").attr({"style": "text-align: center;"}))
                // Build color scale
                heatColor = d3.scaleLinear()
                  .range(["blue", "white"])
                  .domain([45, 20]) // fix to max and min
              }
          else{
                $(divPlacement).append($("<h5/>").html("SARS CT Heatmap").attr({"style": "text-align: center;"}))
                // Build color scale
                heatColor = d3.scaleLinear()
                  .range(["red", "white"])
                  .domain([45, 10]) // fix to max and min
              }

          if (platePassed){
              $(divPlacement).append($("<p/>").html(outputAccuracySummaryString).attr({"style": "text-align: center; display:inline-block;width: 58%; margin: 0% 21% 0% 21%; color: green"}))
          }
          else{
            $(divPlacement).append($("<p/>").html(outputAccuracySummaryString).attr({"style": "text-align: center; display:inline-block;width: 58%; margin: 0% 21% 0% 21%; color: red"}))
          }

            //Read the data

            var tooltip = d3.select(divPlacement)
                            .append("div")
                            .style("opacity", 0)
                            .attr("class", "tooltip")
                            .style("background-color", "white")
                            .style("border", "solid")
                            .style("border-width", "2px")
                            .style("border-radius", "5px")
                            .style("padding", "5px")
            var mouseover = function(d) {
                tooltip
                  .style("opacity", 1)
                d3.select(this)
                  .style("stroke-width", "2")
                  .style("opacity", 0.2)
              }
              var mousemove = function(d, i) {
                // console.log(d)
                let rowId = $(this).attr('id')[0]
                let colId = $(this).attr('id').slice(1)

                if (i[colId][rowId] != null){
                tooltip
                  .html("The CT value of<br>" + rowId + colId + " is: " + Math.round(i[colId][rowId] * 100) / 100)
                  .style("left", (d3.pointer(d)[0]) + "px")
                  .style("top", (d3.pointer(d)[1]+35) + "px")
              }
                else{
                tooltip
                  .html("The CT value of<br>" + rowId + colId + " is: N/A")
                  .style("left", (d3.pointer(d)[0]) + "px")
                  .style("top", (d3.pointer(d)[1]+35) + "px")
              }
            }
              var mouseleave = function(d) {
                tooltip
                  .style("opacity", 0)
                d3.select(this)
                  .style("stroke-width", "1")
                  .style("opacity", 1)
              }



                for (var columnCount = 1; columnCount <= 24; columnCount++) {
                  for (var rowCount = 0; rowCount < 16; rowCount++) {
                    let wellId =  rows[rowCount] + columns[columnCount - 1]

                    d3.select("#"+heatMapID).selectAll("wellPositions") //heatMapGrid2
                      .data([sarsDfasObj])
                      .enter()
                      .append("rect")
                      .attr("id", wellId)
                      .attr("x", function() {
                        return x(columnCount)
                      })
                      .attr("y", function(d) {
                        return y(rows[rowCount])
                      })
                      .attr("width", x.bandwidth())
                      .attr("height", y.bandwidth())
                      .attr("style", "stroke:black;stroke-width:1")
                      .style("fill", function(d) {
                        if (d[columnCount][rows[rowCount]] >= 40 || d[columnCount][rows[rowCount]] == null) { 
                          return "white"
                        } else {
                          return heatColor(d[columnCount][rows[rowCount]])
                        }
                      })
                      .on("mouseover", mouseover)
                      .on("mousemove", mousemove)
                      .on("mouseleave", mouseleave)
                  }
            }
}

//---------------------------------------------------------------------------------------------------
async function onClickValidationTypeButton(value){
  $('.textValidationType').append("<span/>").html(value);
  textValidationType = value;
}

//---------------------------------------------------------------------------------------------------
async function onClickPlateTypeButton(value){
  $('.textPlateType').html(value);
  textPlateType = value;

  if (textPlateType == 96){
    $('.yesOption').addClass('disabled')
    $('.textQuadrantSplitType').html("No");
    textQuadrantSplitType = "No";
  }

  else if (textPlateType == 384){
    $('.yesOption').removeClass('disabled')
   // $('.split384').data('toggle', '');
 }

}

//---------------------------------------------------------------------------------------------------
async function onClickQuadrantSplitButton(value){
  $('.textQuadrantSplitType').html(value);
  textQuadrantSplitType = value;
}

//---------------------------------------------------------------------------------------------------
async function onClickChooseFileButton(){
  // console.log("GO!")
  var path = await eel.pythonGoButtonClicked()();
   if (path) {
     // console.log(path);
     $(".fileTextBox").val(path)
     filePath = path
   }
}
//---------------------------------------------------------------------------------------------------

function addPageNav2HeatMapCarousel(sarsDfasObjQuads, calRedDfasObjQuads, outputSummaryString, platePassed){
  // work on fresh start
   $('.sarsDivPlacement').empty()
   $('.calRedDivPlacement').empty()
   $('.pageNavQuads').empty()

   $('.hud').append($("<nav/>").addClass("pageNavQuads").attr({"aria-label": "Page navigation"})
                                  .append($("<ul/>").addClass("pagination justify-content-center").attr({"style": "padding-top: 20%;"})
                                          .append($("<li/>").addClass("page-item shadow-sm")
                                                  .append($("<a/>").addClass("page-link").attr({"href": "#"}).html("1").click(function(){makeOutputHeatMap(sarsDfasObjQuads[0], ".sarsDivPlacement", "heatMapGrid", outputSummaryString[0], platePassed[0]);
                                                                                                                                         makeOutputHeatMap(calRedDfasObjQuads[0], ".calRedDivPlacement", "heatMapGrid2", outputSummaryString[0], platePassed[0])})
                                                         )
                                                  )
                                          .append($("<li/>").addClass("page-item shadow-sm")
                                                  .append($("<a/>").addClass("page-link").attr({"href": "#"}).html("2").click(function(){makeOutputHeatMap(sarsDfasObjQuads[1], ".sarsDivPlacement", "heatMapGrid", outputSummaryString[1], platePassed[1]);
                                                                                                                                         makeOutputHeatMap(calRedDfasObjQuads[1], ".calRedDivPlacement", "heatMapGrid2", outputSummaryString[1], platePassed[1])})
                                                          )
                                                  )
                                          .append($("<li/>").addClass("page-item shadow-sm")
                                                  .append($("<a/>").addClass("page-link").attr({"href": "#"}).html("3").click(function(){makeOutputHeatMap(sarsDfasObjQuads[2], ".sarsDivPlacement", "heatMapGrid", outputSummaryString[2], platePassed[2]);
                                                                                                                                         makeOutputHeatMap(calRedDfasObjQuads[2], ".calRedDivPlacement", "heatMapGrid2", outputSummaryString[2], platePassed[2])})
                                                          )
                                                 )
                                          .append($("<li/>").addClass("page-item shadow-sm")
                                                  .append($("<a/>").addClass("page-link").attr({"href": "#"}).html("4").click(function(){makeOutputHeatMap(sarsDfasObjQuads[3], ".sarsDivPlacement", "heatMapGrid", outputSummaryString[3], platePassed[3]);
                                                                                                                                         makeOutputHeatMap(calRedDfasObjQuads[3], ".calRedDivPlacement", "heatMapGrid2", outputSummaryString[3], platePassed[3])})
                                                         )
                                                 )
                                          )
                                )
}


//---------------------------------------------------------------------------------------------------
async function onClickGoButton(){
  if (filePath != null &&  textValidationType != null && textPlateType != null && textQuadrantSplitType != null){
    // your code here.
    // send data
    var jsonReturnFromPython;
    console.log(filePath);
    console.log(textValidationType);
    console.log(textPlateType);
    console.log(textQuadrantSplitType);

    if (textValidationType == "Accuracy" && textPlateType == 96){ // ACCURACY 96
      // make modal pop up here.
      $('#plateMapSubmit').unbind('click');
      $('.pageNavQuads').empty()
      $('#inputMapModal').modal("show")
      initialPlateMap()
      $('#plateMapSubmit').click(function(){compareMapButton()})
    }

    else if (textValidationType == "Accuracy" && textPlateType == 384 && textQuadrantSplitType == "No"){
      $('#plateMapSubmit').unbind('click');
      $('.pageNavQuads').empty()
      $('#inputMapModal').modal("show")
      initialPlateMap384()
      $('#plateMapSubmit').click(function(){compareMapButton384(false)})
    }

    else if (textValidationType == "Accuracy" && textPlateType == 384 && textQuadrantSplitType == "Yes"){
      $('#plateMapSubmit').unbind('click');
      $('.pageNavQuads').empty()
      $('#inputMapModal').modal("show")
      initialPlateMap384()
      $('#plateMapSubmit').click(function(){compareMapButton384(true)}) // do something here// do something here
    }

    else if (textValidationType == "Uniformity" && textPlateType == 96){ // UNIFORMITY 96
      $('.pageNavQuads').empty()
      let dataFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath)();
      let sarsDfasObj = JSON.parse(dataFromPython[0]);
      let calRedDfasObj = JSON.parse(dataFromPython[1]);
      let outputAccuracySummaryString = dataFromPython[2]
      let platePassed = dataFromPython[3]

      console.log(outputAccuracySummaryString)
      console.log(platePassed)

      if (!jQuery.isEmptyObject(sarsDfasObj)){
        console.log(sarsDfasObj)
        makeOutputHeatMap(sarsDfasObj, ".sarsDivPlacement", "heatMapGrid", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
      }
      if (!jQuery.isEmptyObject(calRedDfasObj)){
        console.log(calRedDfasObj)
        makeOutputHeatMap(calRedDfasObj, ".calRedDivPlacement", "heatMapGrid2", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
      }
    }

    else if (textValidationType == "Uniformity" && textPlateType == 384 && textQuadrantSplitType == "No"){
      $('.pageNavQuads').empty()
      let dataFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath)();
      let sarsDfasObj = JSON.parse(dataFromPython[0])
      let calRedDfasObj = JSON.parse(dataFromPython[1])
      let outputAccuracySummaryString = dataFromPython[2]
      let platePassed = dataFromPython[3]

      if (!jQuery.isEmptyObject(sarsDfasObj)){
        makeOutputHeatMap384(sarsDfasObj, ".sarsDivPlacement", "heatMapGrid", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
      }
      if (!jQuery.isEmptyObject(calRedDfasObj)){
        makeOutputHeatMap384(calRedDfasObj, ".calRedDivPlacement", "heatMapGrid2", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
      }
    }

    else if (textValidationType == "Uniformity" && textPlateType == 384 && textQuadrantSplitType == "Yes"){
       let dataFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath)();
       let sarsDfasObjQuads = [JSON.parse(dataFromPython[0]), JSON.parse(dataFromPython[1]), JSON.parse(dataFromPython[2]), JSON.parse(dataFromPython[3])]
       let calRedDfasObjQuads = [JSON.parse(dataFromPython[4]), JSON.parse(dataFromPython[5]), JSON.parse(dataFromPython[6]), JSON.parse(dataFromPython[7])]
       let outputAccuracySummaryString = [dataFromPython[8], dataFromPython[9], dataFromPython[10], dataFromPython[11]]
       let platePassed = [dataFromPython[12], dataFromPython[13], dataFromPython[14], dataFromPython[15]]

       addPageNav2HeatMapCarousel(sarsDfasObjQuads, calRedDfasObjQuads, outputAccuracySummaryString, platePassed)
    }

    else if (textValidationType == "Checkerboard" && textPlateType == 96){
      $('.pageNavQuads').empty()
      let dataFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath)();
      let sarsDfasObj = JSON.parse(dataFromPython[0]);
      let calRedDfasObj = JSON.parse(dataFromPython[1]);
      let outputAccuracySummaryString = dataFromPython[2]
      let platePassed = dataFromPython[3]

      if (!jQuery.isEmptyObject(sarsDfasObj)){
        makeOutputHeatMap(sarsDfasObj, ".sarsDivPlacement", "heatMapGrid", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
      }
      if (!jQuery.isEmptyObject(calRedDfasObj)){
        makeOutputHeatMap(calRedDfasObj, ".calRedDivPlacement", "heatMapGrid2", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
      }
    }

    else if (textValidationType == "Checkerboard" && textPlateType == 384 && textQuadrantSplitType == "No"){
      $('.pageNavQuads').empty()
      let dataFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath)();
      let sarsDfasObj = JSON.parse(dataFromPython[0])
      let calRedDfasObj = JSON.parse(dataFromPython[1])
      let outputAccuracySummaryString = dataFromPython[2]

      let platePassed = dataFromPython[3]

      if (!jQuery.isEmptyObject(sarsDfasObj)){
        makeOutputHeatMap384(sarsDfasObj, ".sarsDivPlacement", "heatMapGrid", outputAccuracySummaryString, platePassed) // input .sarsDivPlacement,heatMapGrid
      }
      if (!jQuery.isEmptyObject(calRedDfasObj)){
        makeOutputHeatMap384(calRedDfasObj, ".calRedDivPlacement", "heatMapGrid2", outputAccuracySummaryString, platePassed)  //input .sarsDivPlacement,heatMapGrid
      }
    }


    else if (textValidationType == "Checkerboard" && textPlateType == 384 && textQuadrantSplitType == "Yes"){
         $('.pageNavQuads').empty()
         let dataFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath)();
         let sarsDfasObjQuads = [JSON.parse(dataFromPython[0]), JSON.parse(dataFromPython[1]), JSON.parse(dataFromPython[2]), JSON.parse(dataFromPython[3])]
         let calRedDfasObjQuads = [JSON.parse(dataFromPython[4]), JSON.parse(dataFromPython[5]), JSON.parse(dataFromPython[6]), JSON.parse(dataFromPython[7])]
         let outputAccuracySummaryString = [dataFromPython[8], dataFromPython[9], dataFromPython[10], dataFromPython[11]]
         let platePassed = [dataFromPython[12], dataFromPython[13], dataFromPython[14], dataFromPython[15]]

         addPageNav2HeatMapCarousel(sarsDfasObjQuads, calRedDfasObjQuads, outputAccuracySummaryString, platePassed)
      }



  }

  else{ // do something if one of the values are undefined.

    console.log('nothing input')
  }

}
//---------------------------------------------------------------------------------------------------

function addDropButtons(){
  // console.log('FIXME: add dropdown buttons')
  $('.hud').append($("<div/>").addClass("row")
                    .append($("<div/>").addClass("col-12")
                            .append($("<div/>").addClass("input-group mb-3").attr({"style": "display:table; text-align: center;"})
                                    .append($("<div/>").addClass("custom-file")
                                            .append($("<button/>").addClass("btn btn-outline-dark").attr({"type": "button", "id": "inputGroupFile02"}).html("Choose File").click(function(){onClickChooseFileButton()}))
                                            .append($("<input/>").addClass("fileTextBox").attr({"disabled": true}))
                                          )
                                  )
                           )
                  )
// <div id="my_dataviz"></div>
          .append($("<div/>").addClass("dropDownRow row").attr({"style": "padding-top: 0px"})
                          .append($("<div/>").addClass("col-3").attr({"style": "text-align: center;"})
                                  .append($("<div/>").addClass("btn-group")
                                          .append($("<button/>").addClass("btn btn-primary dropdown-toggle animate__animated animate__fadeInUp").attr({'data-toggle': "dropdown", "aria-haspopup": "true", "aria-expanded": "false"}).html("Validation Type"))
                                          .append($("<div/>").addClass("dropdown-menu")
                                                  .append($("<a/>").addClass("dropdown-item").attr({"href":"#"}).html("Accuracy").click(function(){onClickValidationTypeButton("Accuracy")}))
                                                  .append($("<a/>").addClass("dropdown-item").attr({"href":"#"}).html("Checkerboard").click(function(){onClickValidationTypeButton("Checkerboard")}))
                                                  .append($("<a/>").addClass("dropdown-item").attr({"href":"#"}).html("Uniformity").click(function(){onClickValidationTypeButton("Uniformity")}))
                                                        )
                                          )
                                  )



                          .append($("<div/>").addClass("col-3").attr({"style": "text-align: center;"})
                                  .append($("<div/>").addClass("btn-group")
                                          .append($("<button/>").addClass("btn btn-info dropdown-toggle animate__animated animate__fadeInUp").attr({'data-toggle': "dropdown", "aria-haspopup": "true", "aria-expanded": "false"}).html("Plate Type"))
                                          .append($("<div/>").addClass("dropdown-menu")
                                                  .append($("<a/>").addClass("dropdown-item").attr({"href":"#"}).html("96").click(function(){onClickPlateTypeButton(96)}))
                                                  .append($("<a/>").addClass("dropdown-item").attr({"href":"#"}).html("384").click(function(){onClickPlateTypeButton(384)}))
                                                  )
                                          )
                                 )



                          .append($("<div/>").addClass("col-3").attr({"style": "text-align: center;"})
                                  .append($("<div/>").addClass("btn-group")
                                          .append($("<button/>").addClass("btn btn-danger dropdown-toggle animate__animated animate__fadeInUp").attr({'data-toggle': "dropdown", "aria-haspopup": "true", "aria-expanded": "false"}).html("Split Quadrants"))
                                          .append($("<div/>").addClass("split384 dropdown-menu")
                                                  .append($("<a/>").addClass("yesOption dropdown-item").attr({"href":"#"}).html("Yes").click(function(){onClickQuadrantSplitButton("Yes")}))
                                                  .append($("<a/>").addClass("dropdown-item").attr({"href":"#"}).html("No").click(function(){onClickQuadrantSplitButton("No")}))
                                                  )
                                          )
                                )


                          .append($("<div/>").addClass("col-3 goButton").attr({"style": "text-align: center;"})
                                  .append($("<button/>").addClass("btn btn-outline-success animate__animated animate__fadeInUp").html("Go").click(function(){onClickGoButton()}))
                                )

                        )

              .append($("<div/>").addClass("textRow row").attr({"style": "padding-top: 0px"})
                                  .append($("<div/>").addClass("textValidationType col-3").attr({"style": "text-align: center;"}))
                                  .append($("<div/>").addClass("textPlateType col-3").attr({"style": "text-align: center;"}))
                                  .append($("<div/>").addClass("textQuadrantSplitType col-3").attr({"style": "text-align: center;"}))
                      )
 // ----------------- ADD CAROUSEL HEREEE
              .append($("<div/>").addClass("carousel slide").attr({"id": "MapCarouselIndicators", "data-ride":"carousel"})
                                .append($("<ol/>").addClass("carousel-indicators")
                                                  .append($("<li/>").addClass("active").attr({"data-target":"MapCarouselIndicators", "data-slide-to": "0"}))
                                                  .append($("<li/>").attr({"data-target":"MapCarouselIndicators", "data-slide-to": "1"}))
                                       )
                                .append($("<div/>").addClass("carousel-inner")
                                                   .append($("<div/>").addClass("carousel-item active sarsDivPlacement")
                                                                      .append($("<div/>").addClass("tooltip")))
                                                   .append($("<div/>").addClass("carousel-item calRedDivPlacement")
                                                                      .append($("<div/>").addClass("tooltip")))
                                       )
                                .append($("<a/>").addClass("carousel-control-prev").attr({"href":"#MapCarouselIndicators", "role":"button", "data-slide":"prev"})
                                                 .append($("<span/>").addClass("carousel-control-prev-icon").attr({"aria-hidden": "true"}))
                                                 // .append($("<span/>").addClass("sr-only"))
                                      )
                                .append($("<a/>").addClass("carousel-control-next").attr({"href":"#MapCarouselIndicators", "role":"button", "data-slide":"next"})
                                                  .append($("<span/>").addClass("carousel-control-next-icon").attr({"aria-hidden": "true"}))
                                                  // .append($("<span/>").addClass("sr-only"))
                                      )
                      )
}
