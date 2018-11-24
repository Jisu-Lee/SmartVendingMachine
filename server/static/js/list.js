/*
var list = [[1, "cosmetic 1", 11037, 3.4, null, true],
      [2, "cosmetic 2", 11037, 3.4, null,  false],
      [3, "cosmetic 3", 11037, 3.4, null,  true]];
      */

//modify
function addDynamicCosmetic(NO, name, price, score, type, fav_flag){
  imgNo = (Math.floor(Math.random() * 10)) % 3 + 1;
  console.log(type+"_"+imgNo);
  var template = '<div class="col-md-4 col-sm-6 col-xs-6 col-xxs-12 work-item"><a class="rate" id="cosmetic'+NO+'"><img src="/static/images/'+type+"_"+imgNo+'.jpg") }}" alt="cosmetic img" class="img-responsive"><h3 class="fh5co-work-title">'+name+'</h3>$'+price+'</a><span class="fa fa-star " id="cos'+NO+'" style="float: right">'+' '+score+'</span></div>';
  $(".data").append(template);
  if(fav_flag != -1){
    $('#cos'+NO).css("color", "orange");
  }
};

function setModalData(){

  var template = '<div id="modal_data"><h1>Please Rate Me!</h1><fieldset class="rating"><input type="radio" id="star5" name="rating" value="5" /><label class = "full" for="star5" title="Awesome - 5 stars"></label><input type="radio" id="star4half" name="rating" value="4.5" /><label class="half" for="star4half" title="Pretty good - 4.5 stars"></label><input type="radio" id="star4" name="rating" value="4" /><label class = "full" for="star4" title="Pretty good - 4 stars"></label><input type="radio" id="star3half" name="rating" value="3.5" /><label class="half" for="star3half" title="Meh - 3.5 stars"></label><input type="radio" id="star3" name="rating" value="3" /><label class = "full" for="star3" title="Meh - 3 stars"></label><input type="radio" id="star2half" name="rating" value="2.5" /><label class="half" for="star2half" title="Kinda bad - 2.5 stars"></label><input type="radio" id="star2" name="rating" value="2" /><label class = "full" for="star2" title="Kinda bad - 2 stars"></label><input type="radio" id="star1half" name="rating" value="1.5" /><label class="half" for="star1half" title="Meh - 1.5 stars"></label><input type="radio" id="star1" name="rating" value="1" /><label class = "full" for="star1" title="Sucks big time - 1 star"></label><input type="radio" id="starhalf" name="rating" value="0.5" /><label class="half" for="starhalf" title="Sucks big time - 0.5 stars"></label></fieldset><br><br></div>';

  $("#modal_data").remove();
  $(".modal-content").append(template);
}

$(document).ready(function() {


  $(document).on('click', '.fa-star', function (e) {
          //e.stopPropagation();
        var cosmetic_id = this.id; //cosmetic id
        if($('#'+cosmetic_id).css("color") == "rgb(255, 165, 0)"){
                              //favorite


                              cosmetic_id = parseInt(cosmetic_id.replace("cos", ""));
                              var myObj = new Object();

                              alert(user_id+"/"+cosmetic_id+"/-1");

                              var rate_data = [user_id, cosmetic_id, -1];  //id = userID, data = cosmeticID
                              myObj.data = rate_data;
                              var jsonText =  JSON.stringify(myObj);
                              console.log(jsonText);
                              $.ajax({
                                                  url: '/updatefav',
                                                  data: jsonText,
                                                  type: 'POST',
                                                  dataType: "json",
                                                  contentType: 'application/json;charset=UTF-8',
                                                  success: function(response) {
                                                      console.log(response);
                                                      if(reponse["status"] == "ok"){
	                                                    $('#'+cosmetic_id).css("color", "gray");
	                                                    window.location.href='http://127.0.0.1:8080/list'
                                                      }

                                                  },
                                                  error: function(error) {
                                                      console.log(error);
                                                  }
                                              });


           //var fav_data = [user_id, cosmetic_id, true];  //id = userID, data = cosmeticID
        } else{
                            //favorite cancle
              var modal = document.getElementById('myModal');
              // Get the <span> element that closes the modal
              var span = document.getElementsByClassName("close")[0];
              modal.style.display = "block";
              setModalData();
              // When the user clicks the button, open the modal
              // When the user clicks on <span> (x), close the modal
              span.onclick = function() {
                  $("#modal_data").remove();
                  console.log(e);
                  modal.style.display = "none";
                }

                // When the user clicks anywhere outside of the modal, close it
                window.onclick = function(event) {
                   if (event.target == modal) {
                     $("#modal_data").remove();
                     modal.style.display = "none";
                   }
                 }

                 $('input[name="rating"]').off().on('click', function() {
                    console.log(e);


                    console.log(cosmetic_id);
                    var rate_score = this.value;
                    cosmetic_id = parseInt(cosmetic_id.replace("cos", ""));
                    var myObj = new Object();

                    alert(user_id+"/"+cosmetic_id+"/"+rate_score);

                    var rate_data = [user_id, cosmetic_id, rate_score];  //id = userID, data = cosmeticID
                    myObj.data = rate_data;
                    var jsonText =  JSON.stringify(myObj);
                    console.log(jsonText);
                    $.ajax({
                                        url: '/updatefav',
                                        data: jsonText,
                                        type: 'POST',
                                        dataType: "json",
                                        contentType: 'application/json;charset=UTF-8',
                                        success: function(response) {
                                            console.log(response);
                                        	if(response["status"] == "ok"){
                                            	
                                            	$('#'+cosmetic_id).css("color", "orange");
                                            	alert("영은이귀엽다");
                                        	window.location.href='http://127.0.0.1:8080/list'}
                                        },
                                        error: function(error) {
                                            console.log(error);
                                        }
                                    });

                                modal.style.display = "none";

                            });
           //$('#'+cosmetic_id).css("color", "orange");
           //var fav_data = [user_id, cosmetic_id, false];  //id = userID, data = cosmeticID
        }


          /////



        /*  $.ajax({
                  url: '/updatefav',
                  data: jsonText,
                  type: 'POST',
                  dataType: "json",
                  contentType: 'application/json;charset=UTF-8',
                  success: function(response) {
                      console.log(response);
                  },
                  error: function(error) {
                      console.log(error);
                  }
              });*/

      });

$(document).on('click', '.rate', function (e) {



});

/*
var list = [[1, "cosmetic 1", 11037, 3.4, null, true],
      [2, "cosmetic 2", 11037, 3.4, null,  false],
      [3, "cosmetic 3", 11037, 3.4, null,  true]];
      */
for(var i=0; i<list.length; i++){
	addDynamicCosmetic(i+1, list[i][1], list[i][2], list[i][3], list[i][4], list[i][5]);
}
});
