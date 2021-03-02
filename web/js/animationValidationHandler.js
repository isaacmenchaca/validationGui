// const hudContainer = document.getElementById("container") // vanilla js
// addEventListener is v js




// hudContainer.addEventListener('animationend', function(){
//     setTimeout(function(){ // wait for x ms until next action.
//         hudContainer.remove(); }, 2000);
//     // setTimeout(function(){
//     //     mainEntry.style.display = 'block';
//     // }, 4000)
//
//     // start adding the buttons
//
//     console.log("Animation ends for logo pic.");
// });


$( document ).ready(function() {
    $('.hud').one("animationend", function(){
        setTimeout(function() {
          // now start adding the dropdown.
          addDropButtons();
          // $('#container').remove(); use this to remove
        }, 0);
      }
    ); // jquery selector
});


var textValidationType;
var textPlateType
var textQuadrantSplitType;
var filePath;


async function onClickValidationTypeButton(value){
  $('.textValidationType').append("<span/>").html(value);
  textValidationType = value;
}

async function onClickPlateTypeButton(value){
  $('.textPlateType').html(value);
  textPlateType = value;
}

async function onClickQuadrantSplitButton(value){
  $('.textQuadrantSplitType').html(value);
  textQuadrantSplitType = value;
}

async function onClickChooseFileButton(){
  // console.log("GO!")
  var path = await eel.pythonGoButtonClicked()();
   if (path) {
     // console.log(path);
     $(".fileTextBox").val(path)
     filePath = path
   }
}

async function onClickGoButton(){
  // send data
  console.log(filePath);
  console.log(textValidationType);
  console.log(textPlateType);
  console.log(textQuadrantSplitType);
  // do something if one of the values are undefined.
  await eel.getValidationInputs(textValidationType, textPlateType, textQuadrantSplitType, filePath)
}

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

  $('.hud').append($("<div/>").addClass("dropDownRow row").attr({"style": "padding-top: 0px"})
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
                                          .append($("<div/>").addClass("dropdown-menu")
                                                  .append($("<a/>").addClass("disabled dropdown-item").attr({"href":"#"}).html("Yes").click(function(){onClickQuadrantSplitButton("Yes")}))
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


}
