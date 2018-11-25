
function addDynamicCosmetic(NO, name, price, score, type, fav_flag){
  imgNo = (Math.floor(Math.random() * 10)) % 3 + 1;
  var template = '<div class="col-md-4 col-sm-6 col-xs-6 col-xxs-12 work-item"><a class="rate" id="cosmetic'+NO+'"><img src="/static/images/'+type+"_"+imgNo+'.jpg") }}" alt="cosmetic img" class="img-responsive"><h3 class="fh5co-work-title">'+name+'</h3>$'+price+'</a><span class="fa fa-star " id="cos'+NO+'" style="float: right">'+' '+score+'</span></div>';
  $("#"+type).append(template);

  if(fav_flag == "true"){
    $('.fa-star').css("color","orange");
  }
};


 function setModalData_detail(idx){
 for(var i=0; i<recommanded_cos.length; i++){
   if(parseInt(recommanded_cos[i]["id"]) == idx){
     var template = '<br class="dt"><h4 class="dt">Product Name: '+recommanded_cos[i]["name"]+'</h4><h4 class="dt">Skin Type: '+recommanded_cos[i]["skintype"]+'</h4><h4 class="dt">Product Type: '+recommanded_cos[i]["product_type"]+'</h4><h4 class="dt">Price: $'+recommanded_cos[i]["price"]+'</h4><h4 class="dt">Score: '+recommanded_cos[i]["rating"]+'</h4>';

   }
 }
   $(".dt").remove();
   $(".modal-content").append(template);
 }

$(document).ready(function() {
  $(document).on('click', '.rate', function (e) {


    console.log(this.id);
    var idx = parseInt(this.id.replace("cosmetic", ""));
    var template = '<p></p>'
    //setModalData_detail();
  //$("#modal-content_detail").empty();

  console.log(idx);
  var modal = document.getElementById('myModal');
  // Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[0];
  modal.style.display = "block";
  setModalData_detail(idx);
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


  });

	for(var i=0; i<recommanded_cos.length; i++){
		ptype = (recommanded_cos[i]["product_type"]).toUpperCase();
		if(ptype == "SUNSCREEN"){
			recommanded_cos[i]["product_type"] = "sunblock";
		}
		else if(ptype == "MOSITURIZER"){
			recommanded_cos[i]["product_type"] = "skin";
		}else if(ptype == "CREAM"){
			recommanded_cos[i]["product_type"] = "lotion";
		}
	addDynamicCosmetic(recommanded_cos[i]["id"], recommanded_cos[i]["name"], recommanded_cos[i]["price"], recommanded_cos[i]["rating"], recommanded_cos[i]["product_type"], recommanded_cos[i]["fav_flag"]);
	}

});
