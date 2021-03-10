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
  d3.select("#inputPlate").selectAll('svg').remove();

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

//---------------------------------------------------------------------------------------------------
function changeWellColor(wellPosID, rowCount, columnCount){
              // console.log(wellPos)
              // console.log(wellPosID)

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

  // $("#inGrid").forEach(function(entry) {
  //   console.log(entry);
  // });

  var negCount = 0
  var cps100Count = 0
  var cps200Count = 0
  var cps2000Count = 0
  var cps20000Count = 0
  var plateMapColorArray = new Array(96);

  $("rect").each( function( index, element ){
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
    let sarsDfFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath, plateMapColorArray)();
    let sarsDfasObj = JSON.parse(sarsDfFromPython);

    console.log(sarsDfFromPython) // returns JSON in string
    console.log(typeof sarsDfFromPython)


    if (!jQuery.isEmptyObject(sarsDfasObj)){
      console.log(sarsDfasObj)
      makeOutputHeatMap(sarsDfasObj)
      // console.log(typeof asObj)
    }


    $('#inputMapModal').modal("hide")
  }
  else{
    console.log("Dont pass that data.", negCount, cps100Count, cps200Count, cps2000Count, cps20000Count)
  }
  // console.log(plateMapColorArray)
}

//---------------------------------------------------------------------------------------------------
function makeOutputHeatMap(sarsDfasObj){


    let rows = ["A", "B", "C", "D", "E", "F", "G", "H"];
    let columns = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"];
    let margin = {top: 30, right: 30, bottom: 30, left: 30};
    let width = (125 * 5) - margin.left - margin.right;
    let height = (82 * 5) - margin.top - margin.bottom;

    let svg = d3.select(".sarsDivPlacement")
            .append("svg")
            .attr("id", "heatMapSvg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("id", "heatMapGrid")
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

          // Build color scale
          let heatColor = d3.scaleLinear()
            .range(["red", "white"])
            .domain([45, 20])

            //Read the data
                for (var columnCount = 1; columnCount <= 12; columnCount++) {
                  for (var rowCount = 0; rowCount < 8; rowCount++) {
                    d3.select("#heatMapGrid").selectAll()
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
                        if (d[columnCount][rows[rowCount]] >= 40) {
                          return heatColor(null)
                        } else {
                          return heatColor(d[columnCount][rows[rowCount]])
                        }
                      })
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
async function onClickGoButton(){
  if (filePath != null &&  textValidationType != null && textPlateType != null && textQuadrantSplitType != null){
    // your code here.
    // send data
    var jsonReturnFromPython;
    console.log(filePath);
    console.log(textValidationType);
    console.log(textPlateType);
    console.log(textQuadrantSplitType);

    if (textValidationType == "Accuracy"){
     // hide
      // make modal pop up here.
      $('#inputMapModal').modal("show")
      // <button type="plateMapSubmit button" class="reload btn btn-primary">Submit</button>
      initialPlateMap()
      $('#plateMapSubmit').click(function(){compareMapButton()})

      // $('.modal-footer').append($("<button/>").addClass("btn btn-primary").attr({"type": "button", "id": "plateMapSubmit"}).html("Submit").click(function(){compareMapButton()})



      // obtain value of modal pop up to mapInput and then push the variable into a function.
      //jsonReturnFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath)()
    }
    else{
      console.log("else stuff activated")
      jsonReturnFromPython = await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath)()
      console.log(jsonReturnFromPython)
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
                                                   .append($("<div/>").addClass("carousel-item active sarsDivPlacement"))
                                                   .append($("<div/>").addClass("carousel-item calRedDivPlacement"))
                                // <div class="carousel-item active">
                                //       <img class="d-block w-100" src="..." alt="First slide">
                                //     </div>
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


                      // <div id="MapCarouselIndicators" class="carousel slide" data-ride="carousel">
                      //      <ol class="carousel-indicators">
                      //        <li data-target="#MapCarouselIndicators" data-slide-to="0" class="active"></li>
                      //        <li data-target="#MapCarouselIndicators" data-slide-to="1"></li>
                      //      </ol>
                      //      <div class="carousel-inner">
                      //        <div class="carousel-item active sarsDivPlacement">
                      //           <!-- <img class="d-block w-100" src="..." alt="First slide"> -->
                      //       </div>
                      //     </div>
                      // </div>

              // <div id="carouselExampleIndicators" class="carousel slide" data-ride="carousel">
              //   <ol class="carousel-indicators">
              //     <li data-target="#carouselExampleIndicators" data-slide-to="0" class="active"></li>
              //     <li data-target="#carouselExampleIndicators" data-slide-to="1"></li>
              //     <li data-target="#carouselExampleIndicators" data-slide-to="2"></li>
              //   </ol>
              //   <div class="carousel-inner">
              //     <div class="carousel-item active">
              //       <img class="d-block w-100" src="..." alt="First slide">
              //     </div>
              //     <div class="carousel-item">
              //       <img class="d-block w-100" src="..." alt="Second slide">
              //     </div>
              //     <div class="carousel-item">
              //       <img class="d-block w-100" src="..." alt="Third slide">
              //     </div>
              //   </div>
              //   <a class="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
              //     <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              //     <span class="sr-only">Previous</span>
              //   </a>
              //   <a class="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
              //     <span class="carousel-control-next-icon" aria-hidden="true"></span>
              //     <span class="sr-only">Next</span>
              //   </a>
              // </div>

}
