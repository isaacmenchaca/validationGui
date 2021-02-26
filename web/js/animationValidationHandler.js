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
    $('#container').one("animationend", function(){
        setTimeout(function() {
          // now start adding the dropdown.
          addDropButtons();
          // $('#container').remove(); use this to remove
        }, 0);
      }
    ); // jquery selector

});

function addDropButtons(){
  console.log('FIXME: add dropdown buttons')
  $('#container').append($("<div/>").addClass("btn-group")
                          .append($("<button/>").addClass("btn btn-primary dropdown-toggle animate__animated animate__fadeInUp").html("Validation Type"))
                          .append($("<button/>").addClass("btn btn-success dropdown-toggle animate__animated animate__fadeInUp").html("Plate Type"))
                          .append($("<button/>").addClass("btn btn-info  dropdown-toggle animate__animated animate__fadeInUp").html("Split Quadrants?")))

}
